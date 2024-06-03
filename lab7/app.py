import sys
import subprocess
import kazoo as kz
from kazoo.client import KazooClient
from dataclasses import dataclass


@dataclass
class TNode:
    node: str
    children: list[str]


class App:
    def __init__(self, node: str, ext_app: str, hosts: str):
        self.node: str = node
        self.ext_app: str = ext_app
        self.app_proc: subprocess.Popen = None

        self.zk = KazooClient(hosts=hosts)

    def watch_node(self, event):
        print(f'[INFO] "{self.node}" {event.type}')

        match event.type:
            case "CREATED":
                try:
                    self.app_proc = subprocess.Popen(self.ext_app)
                except Exception as e:
                    print(f"[ERROR] Exception occurred while opening app {self.ext_app}: {e}")

                self.zk.get_children_async(
                    path=self.node, watch=lambda e: self.watch_children(TNode(self.node, []), e)
                )

            case "DELETED":
                try:
                    self.app_proc.kill() if self.app_proc is not None else ...
                except Exception as e:
                    print(f"[ERROR] Exception occurred while closing app {self.ext_app}: {e}")

            case _:
                pass

        self.zk.exists_async(path=self.node, watch=self.watch_node)

    def watch_children(self, tnode: TNode, event):
        match event.type:
            case "CHILD":
                try:
                    ch = self.zk.get_children(tnode.node)

                    if len(ch) > len(tnode.children):
                        print(f"[INFO] Child has been created in {tnode.node}")

                        for c in set(ch) - set(tnode.children):
                            path = tnode.node + "/" + c
                            self.zk.get_children_async(
                                path=path, watch=lambda e: self.watch_children(TNode(path, []), e)
                            )
                    else:
                        print(f"[INFO] Child has been deleted in {tnode.node}")

                    self.zk.get_children_async(
                        path=tnode.node, watch=lambda e: self.watch_children(TNode(tnode.node, ch), e)
                    )
                except kz.exceptions.NoNodeError as e:
                    ...
            case _:
                pass

    def tree(self, node: str, header: str = "", last: bool = True) -> str:
        ret = header + ("└──" if last else "├──") + node.split("/")[-1] + "\n"
        for i, c in enumerate(ch := sorted(self.zk.get_children(node))):
            ret += self.tree(node=node + "/" + c, header=header + ("   " if last else "│  "), last=(i == len(ch) - 1))
        return ret

    def mainloop(self) -> None:
        try:
            self.zk.start()
        except Exception as e:
            print(f"[ERROR] Exception occurred during connection to zk: {e}")
            return

        self.zk.exists_async(path=self.node, watch=self.watch_node)

        if self.zk.exists(path=self.node):
            print(f'[INFO] "{self.node}" already exists')

            try:
                self.app_proc = subprocess.Popen(self.ext_app)
            except Exception as e:
                print(f"[ERROR] Exception occurred while opening app {self.ext_app}: {e}")

        try:
            while True:
                command = input("==> ")
                if not command:
                    pass
                elif command == "q":
                    break
                elif command == "tree":
                    if self.zk.exists(path=self.node):
                        print(self.tree(self.node))
                    else:
                        print(f'[INFO] Node "{self.node}" does not exist')
                else:
                    print("Unknown command. Usage:\n List all nodes: ==> tree\n Quit:           ==> q")
        except KeyboardInterrupt:
            ...
        finally:
            self.zk.stop()


if __name__ == "__main__":
    znode = "/a"
    hosts = "127.0.0.1:2181"
    ext_app = "gnome-calculator"
    App(node=znode, ext_app=ext_app, hosts=hosts).mainloop()
