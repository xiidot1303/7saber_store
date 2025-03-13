from rest_framework import serializers
from app.models import Category
from app.models import Subcategory
from app.models import Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en', 'description']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en', 'description', 'category']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en', 'photo', 'description', 'short_description', 'articule', 'subcategory', 'price', 'discount_price']
        depth = 1
