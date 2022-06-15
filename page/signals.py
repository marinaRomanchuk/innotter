from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .tasks import send_message


@receiver(post_save, sender=Post)
def send_email(instance, **kwargs):
    followers = instance.page.followers.values_list("email", flat=True)
    send_message.delay(
        receivers=tuple(followers),
        message=f"Visit Innotter to see new post on page {instance.page.name}.",
    )
