from app.services import *
from app.models import Order, OrderItem


async def get_order_by_id(id: int | str) -> Order | None:
    obj = await Order.objects.filter(id=id).afirst()
    return obj

@sync_to_async
def get_order_items_list_by_order_id(order_id: int | str) -> list | None:
    items = list(OrderItem.objects.filter(order_id=order_id).values(
        'id', 'order_id', 'product_id', 'product__name', 'product__mxik', 'product__package_code', 'color_id', 'size_id', 'quantity', 'price'
    ))
    return items


async def order_pay(order: Order, payment_system):
    order.payed = True
    order.payment_system = payment_system
    await order.asave()