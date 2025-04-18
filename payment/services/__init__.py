from app.services.order_service import (
    get_order_by_id as get_account_by_id,
    order_pay as account_pay,
    get_order_items_list_by_order_id as get_items_by_account_id,
)
from bot.services import notification_service as notify
from app.models import Order as Account
from payment.services.payme.subscribe_api import receipts_create_api as get_payme_invoice_id



async def get_invoice_url(payment_id, amount, payment_system):
    if payment_system == 'Payme':
        # create receipt
        invoice_id = await get_payme_invoice_id(payment_id, amount)
        url = f'https://payme.uz/checkout/{invoice_id}'
    # if payment_system == 'Click':
    #     url = get_click_invoice_url(payment_id, amount)
    # if payment_system == 'Uzum':
    #     url = get_uzum_invoice_url(payment_id, amount)
    return url