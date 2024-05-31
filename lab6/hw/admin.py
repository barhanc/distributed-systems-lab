import threading
import pika


def receive_logs():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="requests_exchange", exchange_type="topic")
    channel.exchange_declare(exchange="results_exchange", exchange_type="topic")
    queue_name = "logs_queue"
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange="requests_exchange", queue=queue_name, routing_key="#")
    channel.queue_bind(exchange="results_exchange", queue=queue_name, routing_key="#")

    def callback(ch, method, properties, body):
        print(f"[LOG] {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


# Receiving info thread
info_thread = threading.Thread(target=receive_logs, args=())
info_thread.daemon = True
info_thread.start()

# Sending info thread
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="info_exchange", exchange_type="fanout")

try:
    while True:
        message = input("=> ")
        channel.basic_publish(exchange="info_exchange", routing_key="", body=message)

except KeyboardInterrupt:
    print("Interrupted")
