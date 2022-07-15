from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Post
from .tasks import send_message
from .producer import publish


@receiver(post_save, sender=Post)
def send_email(instance, **kwargs):
    followers = instance.page.followers.values_list("email", flat=True)
    send_message.delay(
        receivers=tuple(followers),
        message=f"Visit Innotter to see new post on page {instance.page.name}.",
    )


@receiver(post_save, sender=Post)
def send_post_creation_message(instance, **kwargs):
    publish(
        "new_post",
        {
            "page_id": str(instance.page.id),
            "post_id": instance.id,
            "field": "posts_number",
            "sign": "+",
        },
    )


@receiver(post_delete, sender=Post)
def send_post_removal_message(instance, **kwargs):
    publish(
        "post_removal",
        {
            "page_id": str(instance.page.id),
            "post_id": instance.id,
            "field": "posts_number",
            "sign": "-",
        },
    )
