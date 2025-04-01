from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Banner
from app.serializers import BannerSerializer

class BannerListView(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)
