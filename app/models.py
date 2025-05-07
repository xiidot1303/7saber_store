from django.db import models
from asgiref.sync import sync_to_async

class Category(models.Model):
    billz_id = models.CharField(max_length=128, null=True, verbose_name="ID Billz")
    name = models.CharField(max_length=255, verbose_name="Название")
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (узбекский)")
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (русский)")
    name_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (английский)")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    index = models.IntegerField(unique=True, null=True, verbose_name="Индекс")
    photo = models.FileField(upload_to='categories/', null=True, blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', null=True, on_delete=models.CASCADE, verbose_name="Категория")
    billz_id = models.CharField(max_length=128, null=True, verbose_name="ID Billz")
    name = models.CharField(max_length=255, verbose_name="Название")
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (узбекский)")
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (русский)")
    name_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (английский)")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='products', null=True, on_delete=models.CASCADE, verbose_name="Подкатегория")
    billz_parent_id = models.CharField(max_length=128, null=True, blank=True, verbose_name="ID Родителя Billz")
    name = models.CharField(max_length=255, null=True, verbose_name="Название")
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (узбекский)")
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (русский)")
    name_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название (английский)")
    photo = models.CharField(max_length=255, null=True, verbose_name="Фото")
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, verbose_name="Цена")
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="Цена со скидкой")
    description = models.TextField(null=True, verbose_name="Описание")
    short_description = models.CharField(max_length=255, null=True, verbose_name="Краткое описание")
    articule = models.CharField(max_length=100, null=True, verbose_name="Артикул")
    mxik = models.CharField(max_length=100, null=True, verbose_name="MXIK")
    package_code = models.CharField(max_length=100, null=True, verbose_name="Код упаковки")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', null=True, on_delete=models.CASCADE, verbose_name="Продукт")
    photo = models.CharField(max_length=255, null=True, verbose_name="Фото")
    color = models.CharField(max_length=50, null=True, verbose_name="Цвет")
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, verbose_name="Цена")
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="Цена со скидкой")

    class Meta:
        verbose_name = "Цвет продукта"
        verbose_name_plural = "Цвета продуктов"

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductSize(models.Model):
    product_color = models.ForeignKey(ProductColor, related_name='sizes', on_delete=models.CASCADE, verbose_name="Цвет продукта")
    size = models.CharField(max_length=255, null=True, verbose_name="Размер")
    dimensions = models.CharField(max_length=10, null=True, verbose_name="Габариты")
    quantity = models.PositiveIntegerField(null=True, verbose_name="Количество")
    weight = models.DecimalField(max_digits=5, decimal_places=0, null=True, verbose_name="Вес")

    class Meta:
        verbose_name = "Размер продукта"
        verbose_name_plural = "Размеры продуктов"

    def __str__(self):
        return f"{self.product_color.product.name} - {self.product_color.color} - {self.size}"

class DeliveryType(models.Model):
    title_uz = models.CharField(max_length=255, null=True, verbose_name="Название (узбекский)")
    title_ru = models.CharField(max_length=255, null=True, verbose_name="Название (русский)")
    title_en = models.CharField(max_length=255, null=True, verbose_name="Название (английский)")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")

    class Meta:
        verbose_name = "Тип доставки"
        verbose_name_plural = "Типы доставки"

    def __str__(self):
        return self.title_en

class Customer(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.first_name

class Order(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Пользователь бота")
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, verbose_name="Клиент")
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE, verbose_name="Тип доставки")
    payment_method = models.CharField(max_length=50, verbose_name="Метод оплаты")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена доставки")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    payed = models.BooleanField(default=False, verbose_name="Оплачено")
    payment_system = models.CharField(max_length=50, blank=True, null=True, verbose_name="Платежная система")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name="Статус")
    sent_to_group = models.BooleanField(default=False, verbose_name="Отправлено в группу")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id} by {self.customer.first_name}"

    @property
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, verbose_name="Цвет")
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, verbose_name="Размер")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.product.name} - {self.color.color} - {self.size.size}"

class Banner(models.Model):
    photo = models.FileField(upload_to='banners/', verbose_name="Фото")

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self):
        return f"Banner {self.id}"
