from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ..models import Like, Comment, Follow, Notification


def create_notification(sender, receiver, notif_type, post=None):
    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        type=notif_type,
        post=post
    )

    # Push to channel layer
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{receiver.id}",
        {
            "type": "send_notification",
            "data": {
                "id": notification.id,
                "type": notification.type,
                "sender": sender.username,
                "post": post.id if post else None,
                "created_at": str(notification.created_at),
            }
        }
    )


@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    if created:
        create_notification(instance.user, instance.post.owner, 'like', post=instance.post)


@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        create_notification(instance.user, instance.post.owner, 'comment', post=instance.post)


@receiver(post_save, sender=Follow)
def notify_on_follow(sender, instance, created, **kwargs):
    if created:
        create_notification(instance.follower, instance.following, 'follow')
