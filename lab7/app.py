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
                self.app_proc = subprocess.Popen(self.ext_app)
                self.zk.get_children(path=self.node, watch=lambda e: self.watch_children(TNode(self.node, []), e))

            case "DELETED":
                self.app_proc.kill() if self.app_proc is not None else ...

            case _:
                pass

        self.zk.exists(self.node, watch=self.watch_node)

    def watch_children(self, tnode: TNode, event):
        match event.type:
            case "CHILD":
                if self.zk.exists(tnode.node):
                    ch = self.zk.get_children(
                        tnode.node, watch=lambda e: self.watch_children(TNode(tnode.node, ch), e)
                    )

                    if len(ch) > len(tnode.children):
                        print(f'[INFO] Child has been created in "{tnode.node}".')
                        print(f"[INFO] Total number of child nodes is {self.cnt_nodes(self.node)-1}")

                        for c in set(ch) - set(tnode.children):
                            node = tnode.node + "/" + c
                            self.zk.get_children(node, watch=lambda e: self.watch_children(TNode(node, []), e))
                    else:
                        print(f'[INFO] Child has been deleted in "{tnode.node}"')

                else:
                    print(f'[INFO] Node "{tnode.node}" has been deleted')
            case _:
                pass

    def tree(self, node: str, header: str = "", last: bool = True) -> str:
        ret = header + ("└──" if last else "├──") + node.split("/")[-1] + "\n"
        for i, c in enumerate(ch := sorted(self.zk.get_children(node))):
            ret += self.tree(node=node + "/" + c, header=header + ("   " if last else "│  "), last=(i == len(ch) - 1))
        return ret

    def cnt_nodes(self, node):
        return 1 + sum(self.cnt_nodes(node + "/" + c) for c in self.zk.get_children(node))

    def set_children_watch(self, node):
        ch = self.zk.get_children(node, watch=lambda e: self.watch_children(TNode(node, ch), e))
        for c in ch:
            self.set_children_watch(node + "/" + c)

    def mainloop(self) -> None:
        self.zk.start()

        if self.zk.exists(self.node, watch=self.watch_node):
            print(f'[INFO] "{self.node}" already exists')
            self.app_proc = subprocess.Popen(self.ext_app)
            self.set_children_watch(self.node)

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
            print("Interrupted")

        finally:
            self.app_proc.kill() if self.app_proc is not None else ...
            self.zk.stop()


if __name__ == "__main__":
    znode = "/a"
    hosts = "127.0.0.1:2181"
    ext_app = sys.argv[1] if len(sys.argv) == 2 else "gnome-calculator"
    App(node=znode, ext_app=ext_app, hosts=hosts).mainloop()
