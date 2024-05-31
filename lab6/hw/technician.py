import threading
import random
import time
import sys
import pika


def receive_info(id: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="info_exchange", exchange_type="fanout")
    queue_name = f"info_{id}_queue"
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange="info_exchange", queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"[INFO] {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


assert len(sys.argv) == 4, "Expected id and two injuries types (hip, elbow or knee) to be passed."
assert len(injuries := set(sys.argv[2:])) == 2, "Expected distinct two injuries types"
assert injuries.issubset({"hip", "elbow", "knee"}), "Injury should be one of: hip, elbow, knee."

id = sys.argv[1]

# Receiving info thread
info_thread = threading.Thread(target=receive_info, args=(id,))
info_thread.daemon = True
info_thread.start()

# Processing requests thread
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="requests_exchange", exchange_type="topic")
channel.exchange_declare(exchange="results_exchange", exchange_type="topic")


def callback_requests(ch, method, properties, body):
    print(f"[x] Received {body.decode()}")
    time.sleep(random.randint(1, 3))
    print(f"[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    msg = f"{body.decode()}.done"
    channel.basic_publish(exchange="results_exchange", routing_key=msg, body=msg)
    print(f"[x] Sent {msg}")


for injury in injuries:
    queue_name = f"{injury}_queue"
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange="requests_exchange", queue=queue_name, routing_key=f"{injury}.*.*")
    channel.basic_consume(queue=queue_name, on_message_callback=callback_requests)

channel.basic_qos(prefetch_count=1)

try:
    print("Waiting for requests...")
    channel.start_consuming()

except KeyboardInterrupt:
    print("Interrupted")
