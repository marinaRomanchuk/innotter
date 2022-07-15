import json
import pika
import os


class Producer:
    def __init__(self):
        self.credentials = pika.PlainCredentials(
            os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD")
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                os.getenv("RABBITMQ_HOST"),
                int(os.getenv("RABBITMQ_PORT")),
                os.getenv("RABBITMQ_VHOST"),
                credentials=self.credentials,
                heartbeat=600,
                blocked_connection_timeout=300,
            )
        )
        self.channel = self.connection.channel()

    def publish(self, queue, body):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(body),
        )


producer = Producer()
