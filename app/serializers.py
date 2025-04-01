from rest_framework import serializers
from app.models import Category, Subcategory, Product, DeliveryType, Banner

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

class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = ['id', 'title_uz', 'title_ru', 'title_en', 'price']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'photo']
