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
        cache.set("billz_access_token", access_token, timeout=86400)
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
                subcategory_id = product['categories'][0]['id'] if product['categories'] else None
                name = product.get("name").split("/")[0].strip()
                main_photo = product.get("main_image_url_full")
                # get quantity
                quantity = None
                for shop_measurement in product.get("shop_measurement_values", []):
                    if shop_measurement['shop_name'] == "Телеграмм бот":
                        quantity = shop_measurement['active_measurement_value']
                        break
                if not quantity:
                    continue
                # get price
                price = None
                for shop_price in product.get("shop_prices", []):
                    if shop_price['shop_name'] == "Телеграмм бот":
                        price = shop_price['retail_price']
                        break
                if not price:
                    continue
                
                # get mxik and package code
                mxik, package_code = None, None
                if custom_fields:=product.get("custom_fields", []):
                    for custom_field in custom_fields:
                        if custom_field["custom_field_id"] == "6d903c74-bee3-48d8-8ca8-d2344df1ffd7":
                            mxik = custom_field["custom_field_value"]
                        elif custom_field["custom_field_id"] == "f9a0e2a8-9d5e-4059-ac32-76a9c5ae1656":
                            package_code = custom_field["custom_field_value"]

                photo = None
                for p in product.get("photos"):
                    if p['is_main']:
                        photo = p['photo_url']
                        break
                size, color = None, None
                if product_attributes:=product['product_attributes']:
                    if len(product_attributes) >=2:
                        if product_attributes[0]['attribute_name'] == 'Размер':
                            size = product_attributes[0]['attribute_value']
                            color = product_attributes[1]['attribute_value']
                        else:
                            size = product_attributes[1]['attribute_value']
                            color = product_attributes[0]['attribute_value']

                        color = color.split(" ")[0].strip()

                subcategory: Subcategory = Subcategory.objects.filter(billz_id=subcategory_id).first()
                product, is_created = Product.objects.get_or_create(billz_parent_id=parent_id, name=name)
                product.subcategory = subcategory
                product.name = name
                product.price = price
                product.mxik = mxik
                product.package_code = package_code
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

def fetch_categories():
    url = "https://api-admin.billz.ai/v2/category"
    access_token = cache.get("billz_access_token") or fetch_and_cache_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    categories = response_data.get("categories", [])
    
    for category in categories:
        category_id = category.get("id")
        category_obj, created = Category.objects.get_or_create(billz_id=category_id)
        category_obj.name = category.get("name")
        category_obj.save()

        for subcategory in category.get("subRows", []):
            subcategory_id = subcategory.get("id")
            subcategory_obj, created = Subcategory.objects.get_or_create(billz_id=subcategory_id)
            subcategory_obj.category = category_obj
            subcategory_obj.name = subcategory.get("name")
            subcategory_obj.save()

        