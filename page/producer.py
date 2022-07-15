import json
import pika
import os

credentials = pika.PlainCredentials(
    os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD")
)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        os.getenv("RABBITMQ_HOST"),
        int(os.getenv("RABBITMQ_PORT")),
        os.getenv("RABBITMQ_VHOST"),
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key="innotter",
        body=json.dumps(body),
        properties=properties,
    )
