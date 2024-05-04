import time
import random
import string
import threading

import grpc
import gen.event_sub_pb2
import gen.event_sub_pb2_grpc

from concurrent.futures import ThreadPoolExecutor


def update(db: list[gen.event_sub_pb2.Article]):
    while True:
        time.sleep(random.randint(5, 10))

        db.append(
            gen.event_sub_pb2.Article(
                articleType=random.choice(list(gen.event_sub_pb2.ArticleType.keys())),
                author="".join(random.choices(string.ascii_letters, k=10)),
                title="".join(random.choices(string.ascii_letters, k=20)),
                summary="".join(random.choices(string.ascii_letters, k=120)),
                comments=[
                    gen.event_sub_pb2.Comment(
                        author="".join(random.choices(string.ascii_letters, k=10)),
                        comment=random.choice(["Nice", "Ok", "Bad"]),
                    )
                    for _ in range(random.randint(1, 4))
                ],
            )
        )

        print("[DB] New article was added to the database")
        print(db[-1])


class EventSubscriptionServicer(gen.event_sub_pb2_grpc.EventSubscriptionServicer):
    def __init__(self, db: list[gen.event_sub_pb2.Article]) -> None:
        self.db = db

    def SubscribeToEvents(self, request: gen.event_sub_pb2.SubscriptionRequest, context):
        i = len(self.db)
        while context.is_active():
            if (j := len(self.db)) != i:
                for article in filter(lambda a: a.articleType == request.articleType, self.db[i:j]):
                    yield article
                i = j

        print("RPC is not active")


if __name__ == "__main__":
    db: list[gen.event_sub_pb2.Article] = []
    update_thread = threading.Thread(target=update, args=(db,))
    update_thread.daemon = True
    update_thread.start()

    server_options = [
        ("grpc.keepalive_time_ms", 20000),
        ("grpc.keepalive_timeout_ms", 10000),
    ]
    server = grpc.server(thread_pool=ThreadPoolExecutor(max_workers=10), options=server_options)
    port = 50051

    gen.event_sub_pb2_grpc.add_EventSubscriptionServicer_to_server(EventSubscriptionServicer(db), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[SERVER] Server is listening on port {port}")
    server.wait_for_termination()
