import time
import textwrap
import threading

import grpc
import gen.event_sub_pb2
import gen.event_sub_pb2_grpc

HELP_PROMPT: str = f"""
Unknown command. Usage:

'sub <ArticleType>' subscribe to <ArticleType>. Available types:
                    {', '.join(gen.event_sub_pb2.ArticleType.keys())}

'ls'                list active subscriptions

'q'                 quit
"""

format_notification = (
    lambda article_type, article: f"""
========================================
NEW {article_type} ARTICLE

{article.title}
by
{article.author}

{textwrap.fill(article.summary, width=40)}

Comments\n\n"""
    + "\n".join([f"{comment.author}: {comment.comment}" for comment in article.comments])
    + "\n========================================"
)


def handle(stub: gen.event_sub_pb2_grpc.EventSubscriptionStub, article_type: str):
    while True:
        try:
            for article in stub.SubscribeToEvents(gen.event_sub_pb2.SubscriptionRequest(articleType=article_type)):
                print(format_notification(article_type, article))
        except grpc.RpcError as e:
            match e.code():
                case grpc.StatusCode.OK | grpc.StatusCode.CANCELLED:
                    break
                case _:
                    print(f"Failed to get {article_type} article from server. [{e.code()}] Reconnecting ...")
                    time.sleep(5)


def client(stub):
    subscriptions: list[gen.event_sub_pb2.ArticleType] = []
    handle_threads = []

    try:
        while True:
            command = input(">>> ")
            matched = False

            if command.startswith("sub"):
                for article_type in list(gen.event_sub_pb2.ArticleType.keys()):
                    if command == f"sub {article_type}" and article_type not in subscriptions:
                        matched = True
                        subscriptions.append(article_type)

                        handle_thread = threading.Thread(target=handle, args=(stub, article_type))
                        handle_thread.daemon = True
                        handle_threads.append(handle_thread)
                        handle_thread.start()
                        break

                    elif command == f"sub {article_type}":
                        matched = True
                        print(f"You are already subscribed to {article_type}.")
                        break

            elif command == "ls":
                matched = True
                for sub in subscriptions:
                    print(sub)

            elif command == "q":
                matched = True
                exit(0)

            if not matched and len(command) > 0:
                print(HELP_PROMPT)

    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    port = 50051

    channel_options = [
        ("grpc.keepalive_time_ms", 8000),
        ("grpc.keepalive_timeout_ms", 5000),
    ]
    with grpc.insecure_channel(target=f"localhost:{port}") as channel:
        stub = gen.event_sub_pb2_grpc.EventSubscriptionStub(channel)
        client(stub)
