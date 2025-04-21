from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main
)
from app.views.product import CategoryListView, SubcategoryListView, ProductListView, ProductDetailView, ProductPriceRangeView, ProductFilterByTitleView
from app.views.order import OrderView
from app.views.delivery import DeliveryTypeListView
from app.views.banner import BannerListView  # Add import

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),

    # category list API
    path('api/categories/', CategoryListView.as_view(), name='category-list'),

    # subcategory list API
    path('api/subcategories/<int:category_id>/', SubcategoryListView.as_view(), name='subcategory-list'),

    # product list API
    path('api/products/<int:subcategory_id>/', ProductListView.as_view(), name='product-list'),

    # product detail API
    path('api/product/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),

    # order API
    path('api/order/', OrderView.as_view(), name='order'),
    path('api/order', OrderView.as_view(), name='order'),

    # delivery types API
    path('api/deliverytypes/', DeliveryTypeListView.as_view(), name='delivery-type-list'),

    # banner API
    path('api/banners/', BannerListView.as_view(), name='banner-list'),

    # product price range API
    path('products/price-range/', ProductPriceRangeView.as_view(), name='product-price-range'),

    # product filter by title API
    path('api/products/filter-by-title/', ProductFilterByTitleView.as_view(), name='product-filter-by-title'),
]
