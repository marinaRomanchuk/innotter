import json
import pika
import os

from abc import ABC, abstractmethod
from functools import lru_cache


class AbstractProducer(ABC):
    @abstractmethod
    def publish(self, queue, body):
        """Publishing a message in the message broker"""
        pass


class Producer(AbstractProducer):
    def __init__(self, queue):
        self.queue = queue
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

    def publish(self, body):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=json.dumps(body),
        )


@lru_cache
def get_queue(queue_name: str) -> AbstractProducer:
    return Producer(queue_name)


producer_likes = get_queue("innotter_likes")
producer_posts = get_queue("innotter_posts")
producer_followers = get_queue("innotter_followers")
