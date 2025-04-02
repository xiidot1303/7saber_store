from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import Category, Subcategory, Product
from app.serializers import CategorySerializer, SubcategorySerializer, ProductSerializer
from django.conf import settings
from urllib.parse import quote

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryListView(generics.ListAPIView):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Subcategory.objects.filter(category_id=category_id)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['subcategory_id']
        return Product.objects.filter(subcategory_id=subcategory_id)

class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product_data = ProductSerializer(product).data
            product_data['photo'] = product.photo  # Updated to directly use the CharField value
            product_data['colors'] = []

            for color in product.colors.all():
                color_data = {
                    'id': color.id,
                    'photo': color.photo,  # Updated to directly use the CharField value
                    'color': color.color,
                    'price': color.price,
                    'discount_price': color.discount_price,
                    'sizes': []
                }

                for size in color.sizes.all():  # Include all sizes
                    size_data = {
                        'id': size.id,
                        'size': size.size,
                        'dimensions': size.dimensions,
                        'quantity': size.quantity,
                        'weight': size.weight
                    }
                    color_data['sizes'].append(size_data)

                product_data['colors'].append(color_data)

            product_data['name_uz'] = product.name_uz
            product_data['name_ru'] = product.name_ru
            product_data['name_en'] = product.name_en

            return Response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
