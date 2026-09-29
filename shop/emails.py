from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order


def send_order_confirmation(order):
    """Send order confirmation email to customer"""
    try:
        subject = f"Order Confirmation #{order.id}"
        context = {
            "order": order,
            "items": order.items.all(),
            "site_name": "LunaCart",
        }
        html_message = render_to_string("emails/order_confirmation.html", context)
        text_message = render_to_string("emails/order_confirmation.txt", context)
        
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending order confirmation: {str(e)}")


def send_order_shipped(order):
    """Send order shipped notification email"""
    try:
        subject = f"Your Order #{order.id} Has Been Shipped"
        context = {
            "order": order,
            "site_name": "LunaCart",
        }
        html_message = render_to_string("emails/order_shipped.html", context)
        text_message = render_to_string("emails/order_shipped.txt", context)
        
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending order shipped notification: {str(e)}")


def send_order_delivered(order):
    """Send order delivered notification email"""
    try:
        subject = f"Your Order #{order.id} Has Been Delivered"
        context = {
            "order": order,
            "site_name": "LunaCart",
        }
        html_message = render_to_string("emails/order_delivered.html", context)
        text_message = render_to_string("emails/order_delivered.txt", context)
        
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending order delivered notification: {str(e)}")
