from django.urls import path
from .views import products_view,product_detail_view,category_list

app_name = 'shop'  #для того чтобы использовать в шаблонах {% url 'shop:product_detail' slug=product.slug %} пример 'shop: это имя namespace

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('search/<slug:slug>/', category_list, name='category_list'),
]