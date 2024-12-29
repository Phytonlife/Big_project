from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404
from .models import ProductProxy,Category

# Create your views here.


def products_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {'products': products})

def product_detail_view(request,slug):
    product = ProductProxy.objects.get(slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request,slug):
    category=get_object_or_404(Category,slug=slug)
    products=ProductProxy.objects.select_related().filter(category=category)#select_related для того чтобы обращаться к базам данных 1 раз и загрузить все категорий, это оптимизация
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/category_list.html', context)