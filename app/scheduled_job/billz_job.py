from config import BILLZ_SECRET_TOKEN
import requests
from django.core.cache import cache
from app.services.category_service import *
from app.services.product_service import *

def fetch_and_cache_access_token():
    url = "https://api-admin.billz.ai/v1/auth/login"
    payload = {"secret_token": BILLZ_SECRET_TOKEN}
    response = requests.post(url, json=payload)
    response_data = response.json()
    data = response_data.get("data", {})
    access_token = data.get("access_token")
    if access_token:
        cache.set("billz_access_token", access_token)
    return access_token


def fetch_products():
    url = "https://api-admin.billz.ai/v2/products"
    access_token = cache.get("billz_access_token") or fetch_and_cache_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    page = 1
    while True:
        params = {"page": page}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        if products:=response_data.get("products", []):
            for product in products:
                parent_id = product.get("parent_id")
                subcategory_id = product['categories'][0]['id']
                name = product.get("name").split("/")[0].strip()
                main_photo = product.get("main_image_url_full")
                price = product['shop_prices'][0]['retail_price']
                quantity = product['shop_measurement_values'][0]['active_measurement_value']
                photo = None
                for p in product.get("photos"):
                    if not p['is_main']:
                        photo = p['photo_url']
                        break
                if product_attributes:=product['product_attributes']:
                    if product_attributes[0]['attribute_id'] == '146af27e-edae-44ec-84fd-f6439fbb065d':
                        size = product_attributes[0]['attribute_value']
                        color = product_attributes[1]['attribute_value']
                    else:
                        size = product_attributes[1]['attribute_value']
                        color = product_attributes[0]['attribute_value']

                subcategory: Subcategory = Subcategory.objects.filter(billz_id=subcategory_id).first()
                product, is_created = Product.objects.get_or_create(billz_parent_id=parent_id)
                product.subcategory = subcategory
                product.name = name
                product.price = price
                if main_photo:
                    product.photo = main_photo
                product.save()

                product_color, is_created = ProductColor.objects.get_or_create(product=product, color=color)
                product_color.price = price
                if photo:
                    product_color.photo = photo
                product_color.save()

                product_size, is_created = ProductSize.objects.get_or_create(product_color=product_color, size=size)
                product_size.quantity = quantity
                product_size.save()

        else:
            break
        page += 1

def fetch_subcategories():
    url = "https://api-admin.billz.ai/v2/category"
    access_token = cache.get("billz_access_token") or fetch_and_cache_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    categories = response_data.get("categories", [])
    
    subcategories = []
    existing_billz_ids = set(Subcategory.objects.values_list('billz_id', flat=True))
    for category in categories:
        billz_id = category.get("id")
        name = category.get("name")
        if billz_id not in existing_billz_ids:
            subcategories.append(Subcategory(billz_id=billz_id, name=name))
    
    Subcategory.objects.bulk_create(subcategories)