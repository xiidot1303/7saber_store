from django.contrib import admin
from .models import Category, Subcategory, Product, ProductColor, ProductSize

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    inlines = [ProductSizeInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price', 'discount_price', 'articule', 'short_description')
    search_fields = ('name', 'articule', 'subcategory__name')
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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
