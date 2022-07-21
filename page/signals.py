from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Post
from .tasks import send_message
from message_broker.page_producer import producer_posts


@receiver(post_save, sender=Post)
def send_email(instance, **kwargs):
    followers = instance.page.followers.values_list("email", flat=True)
    send_message.delay(
        receivers=tuple(followers),
        message=f"Visit Innotter to see new post on page {instance.page.name}.",
    )


@receiver(post_save, sender=Post)
def send_post_creation_message(instance, **kwargs):
    producer_posts.publish(
        {
            "page_id": str(instance.page.id),
            "post_id": instance.id,
            "field": "posts_number",
            "event": "save",
        },
    )


@receiver(post_delete, sender=Post)
def send_post_removal_message(instance, **kwargs):
    producer_posts.publish(
        {
            "page_id": str(instance.page.id),
            "post_id": instance.id,
            "field": "posts_number",
            "event": "unsave",
        },
    )
