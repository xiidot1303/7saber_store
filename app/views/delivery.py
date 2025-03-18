from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import DeliveryType
from app.serializers import DeliveryTypeSerializer

class DeliveryTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        delivery_types = DeliveryType.objects.all()
        serializer = DeliveryTypeSerializer(delivery_types, many=True)
        return Response(serializer.data)
