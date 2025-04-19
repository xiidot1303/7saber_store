from bot.bot import *
from bot.services.string_service import *
from bot.control.updater import application
from app.models import Order, OrderItem
from payment.services import get_invoice_url


async def send_invoice_to_user(order: Order):
    bot_user: Bot_user = await order.get_bot_user
    strings = Strings(user_id=bot_user.user_id)

    order_items = await sync_to_async(list)(
        order.items.values(
            'product__name', 'color__color', 'size__size', 'quantity', 'price'
        )
    )
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
                url=await get_invoice_url(order.pk, order.total, order.payment_method)
            )
        ]]
    )
    await application.update_queue.put(
        NewsletterUpdate(
            user_id=bot_user.user_id,
            text=text,
            reply_markup=markup,
        )
    )
