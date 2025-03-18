from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Customer, Order, OrderItem, DeliveryType, Product, ProductColor, ProductSize

class OrderView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_data = data.get('customer')
        items_data = data.get('items')
        delivery_type_id = data.get('deliveryType')
        payment_method = data.get('paymentMethod')
        subtotal = data.get('subtotal')
        delivery_price = data.get('deliveryPrice')
        total = data.get('total')
        notes = data.get('notes')

        # Create customer
        customer = Customer.objects.create(
            first_name=customer_data['firstName'],
            phone=customer_data['phone'],
            address=customer_data['address']
        )

        # Create order
        delivery_type = DeliveryType.objects.get(id=delivery_type_id)
        order = Order.objects.create(
            customer=customer,
            delivery_type=delivery_type,
            payment_method=payment_method,
            subtotal=subtotal,
            delivery_price=delivery_price,
            total=total,
            notes=notes
        )

        # Create order items
        for item_data in items_data:
            product = Product.objects.get(id=item_data['productId'])
            color = ProductColor.objects.get(id=item_data['colorId'])
            size = ProductSize.objects.get(id=item_data['sizeId'])
            OrderItem.objects.create(
                order=order,
                product=product,
                color=color,
                size=size,
                quantity=item_data['quantity'],
                price=item_data['price']
            )

        return Response({'status': 'Order created'}, status=status.HTTP_201_CREATED)
