from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', null=True, on_delete=models.CASCADE)
    billz_id = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='products', null=True, on_delete=models.CASCADE)
    billz_parent_id = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=255, null=True)
    name_uz = models.CharField(max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    photo = models.FileField(upload_to='products/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)    
    description = models.TextField(null=True)
    short_description = models.CharField(max_length=255, null=True)
    articule = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', null=True, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='products/', null=True)
    color = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductSize(models.Model):
    product_color = models.ForeignKey(ProductColor, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10, null=True)
    dimensions = models.CharField(max_length=10, null=True)
    quantity = models.PositiveIntegerField(null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=0, null=True)

    def __str__(self):
        return f"{self.product_color.product.name} - {self.product_color.color} - {self.size}"

class DeliveryType(models.Model):
    title_uz = models.CharField(max_length=255, null=True)
    title_ru = models.CharField(max_length=255, null=True)
    title_en = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.title_en

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name

class Order(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.first_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.color.color} - {self.size.size}"

class Banner(models.Model):
    photo = models.FileField(upload_to='banners/')

    def __str__(self):
        return f"Banner {self.id}"
