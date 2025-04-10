from app.services import *
from app.models import Order


async def get_order_by_id(id: int | str) -> Order | None:
    obj = await Order.objects.filter(id=id).afirst()
    return obj


async def order_pay(order: Order, payment_system):
    order.payed = True
    order.payment_system = payment_system
    await order.asave()