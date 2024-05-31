import threading
import sys
import re
import pika


def receive_results(id: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="results_exchange", exchange_type="topic")
    queue_name = f"results_{id}_queue"
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange="results_exchange", queue=queue_name, routing_key=f"*.*.{id}.done")

    def callback(ch, method, properties, body):
        print(f"[x] {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


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


assert len(sys.argv) == 2, "Invalid number of arguments. Expected id to be passed."

id = sys.argv[1]

# Receiving results thread
results_thread = threading.Thread(target=receive_results, args=(id,))
results_thread.daemon = True
results_thread.start()

# Receiving info thread
info_thread = threading.Thread(target=receive_info, args=(id,))
info_thread.daemon = True
info_thread.start()

# Sending requests thread
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="requests_exchange", exchange_type="topic")

try:
    while True:
        command = input("=> ")

        if not command:
            pass

        elif command == "q":
            break

        elif re.match(r"^(hip|knee|elbow)\.[a-zA-Z0-9]+$", command) is not None:
            msg = command + f".{id}"
            channel.basic_publish(exchange="requests_exchange", routing_key=msg, body=msg)
            print(f" [x] Sent {command}:{command}")

        else:
            print("Unrecognized command. Usage:\n Request: => (hip|knee|elbow).<patientId>\n Quit   : => q")

except KeyboardInterrupt:
    print("Interrupted")
