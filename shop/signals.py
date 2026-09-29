from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Wishlist
from django.contrib.auth.models import User
from .emails import send_order_shipped, send_order_delivered


@receiver(post_save, sender=Wishlist)
def create_wishlist(sender, instance, created, **kwargs):
    pass


@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.get_or_create(user=instance)


@receiver(post_save, sender=Order)
def handle_order_status_change(sender, instance, created, update_fields, **kwargs):
    if not created and update_fields:
        if "status" in update_fields:
            if instance.status == "shipped":
                send_order_shipped(instance)
            elif instance.status == "delivered":
                send_order_delivered(instance)
