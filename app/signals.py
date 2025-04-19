from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Order
from app.services.order_service import order_pay
from asgiref.sync import async_to_sync
from bot.services.notification_service import send_invoice_to_user


@receiver(post_save, sender=Order)
def handle_cash_payment_order(sender, instance, created, **kwargs):
    instance: Order
    created = True
    if created and instance.payment_method == "cash":
        async_to_sync(order_pay)(instance.id)
    else:
        # send invoice to user with order information
        async_to_sync(send_invoice_to_user)(instance)