from bot.bot import *
from bot.services.string_service import *
from bot.control.updater import application
from app.models import Order, OrderItem
from payment.services import get_invoice_url
from config import GROUP_ID
from asgiref.sync import async_to_sync
from celery import shared_task
import requests
from config import WEBHOOK_URL


@shared_task
def send_invoice_to_user(order_id):
    order: Order = Order.objects.get(id=order_id)
    bot_user: Bot_user = order.bot_user
    strings = Strings(user_id=bot_user.user_id)

    order_items = list(order.items.values(
            'product__name', 'color__color', 'size__size', 'quantity', 'price'
        ))
    items_text = "\n".join([
        strings.invoice_item.format(
            product=item['product__name'],
            color=item['color__color'],
            size=item['size__size'],
            quantity=item['quantity'],
            price=item['price']
        ) for item in order_items
    ])

    text = strings.invoice_message.format(
        order_id=order.id,
        customer_name=order.customer.first_name,
        subtotal=order.subtotal,
        delivery_price=order.delivery_price,
        total=order.total,
        items=items_text
    )

    markup = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=strings.pay,
                url=async_to_sync(get_invoice_url)(order.pk, order.total, order.payment_method)
            )
        ]]
    )
    async_to_sync(application.bot.send_message)(
        chat_id=bot_user.user_id,
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )

    

@shared_task
def send_order_info_to_group(order_id: int):
    order: Order = Order.objects.get(id=order_id)
    bot_user: Bot_user = order.bot_user

    order_items = list(
        order.items.values(
            'product__name', 'color__color', 'size__size', 'quantity', 'price'
        )
    )
    items_text = "\n".join([
        f"🔹 {item['product__name']} ({item['color__color']}, {item['size__size']}) x{item['quantity']} - {item['price']} сум"
        for item in order_items
    ])

    text = (
        f"🆕 Новый заказ!\n\n"
        f"🆔 ID заказа: {order.id}\n"
        f"👤 Клиент: {order.customer.first_name}\n"
        f"📞 Телефон клиента: {order.customer.phone}\n"
        f"📍 Адрес клиента: {order.customer.address}\n\n"
        f"📦 Состав заказа:\n{items_text}\n\n"
        f"💵 Сумма заказа: {order.subtotal} сум\n"
        f"🚚 Доставка: {order.delivery_price} сум\n"
        f"💰 Общая сумма: {order.total} сум\n\n"
        f"📅 Дата заказа: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤 Информация о пользователе бота:\n"
        f"🔹 Имя: {bot_user.name}\n"
        f"🔹 Никнейм: {bot_user.firstname}\n"
        f"🔹 Username: @{bot_user.username}\n"
        f"🔹 Телефон: {bot_user.phone}\n"
        f"🔹 Язык: {'Русский' if bot_user.lang == 1 else 'Узбекский'}\n"
        f"🔹 Дата регистрации: {bot_user.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    async_to_sync(application.bot.send_message)(
        chat_id=GROUP_ID,
        text=text,
        parse_mode=ParseMode.HTML
    )
