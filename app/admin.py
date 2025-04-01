from django.contrib import admin
from .models import Category, Subcategory, Product, ProductColor, ProductSize, DeliveryType, Customer, Order, OrderItem, Banner

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_uz', 'name_ru', 'name_en', 'description')
    search_fields = ('name', 'name_uz', 'name_ru', 'name_en')

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_uz', 'name_ru', 'name_en', 'category', 'description')
    search_fields = ('name', 'name_uz', 'name_ru', 'name_en', 'category__name')
    list_filter = ('category',)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    inlines = [ProductSizeInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_uz', 'name_ru', 'name_en', 'subcategory', 'price', 'discount_price', 'articule', 'short_description')
    search_fields = ('name', 'name_uz', 'name_ru', 'name_en', 'articule', 'subcategory__name')
    list_filter = ('subcategory',)
    inlines = [ProductColorInline]

class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'price', 'discount_price')
    search_fields = ('product__name', 'color')
    list_filter = ('product', 'color')
    inlines = [ProductSizeInline]

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product_color', 'size', 'dimensions', 'quantity', 'weight')
    search_fields = ('product_color__product__name', 'size')
    list_filter = ('product_color__product', 'size')

class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'title_en', 'price')
    search_fields = ('title_uz', 'title_ru', 'title_en')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone', 'address')
    search_fields = ('first_name', 'phone', 'address')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_user', 'customer', 'delivery_type', 'payment_method', 'subtotal', 'delivery_price', 'total', 'created_at')
    search_fields = ('customer__first_name', 'delivery_type__title_en', 'payment_method')
    list_filter = ('delivery_type', 'payment_method', 'created_at')
    inlines = [OrderItemInline]

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Banner, BannerAdmin)
