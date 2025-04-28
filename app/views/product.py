from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import Category, Subcategory, Product
from app.serializers import CategorySerializer, SubcategorySerializer, ProductSerializer
from django.conf import settings
from urllib.parse import quote
from django.db.models import Min, Max

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryListView(generics.ListAPIView):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        if category_id:
            result = Subcategory.objects.filter(category_id=category_id)
        else:
            result = Subcategory.objects.all()
        return 

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['subcategory_id']
        queryset = Product.objects.filter(subcategory_id=subcategory_id)

        # Get min_price and max_price from query parameters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        # Filter by price range if provided
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

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

class ProductPriceRangeView(APIView):
    def get(self, request):
        price_range = Product.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        return Response(price_range, status=status.HTTP_200_OK)

class ProductFilterByTitleView(APIView):
    def post(self, request):
        title = request.data.get('title', '')
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(name__icontains=title)
        serialized_products = ProductSerializer(products, many=True).data
        return Response(serialized_products, status=status.HTTP_200_OK)
