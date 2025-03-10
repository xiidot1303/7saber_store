from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to='products/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)    
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    articule = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    photo = models.FileField(upload_to='products/')
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductSize(models.Model):
    product_color = models.ForeignKey(ProductColor, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    dimensions = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product_color.product.name} - {self.product_color.color} - {self.size}"
