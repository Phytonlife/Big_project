from django.contrib import admin
from .models import Product,Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',"parent" ,'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):#Создание уникального слага автоматически
        return {"slug": ("name",)}
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',"brand",'slug','price','aviable','category','created_at','updated_at')
    list_filter = ('aviable',"created_at",'updated_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):#Создание уникального слага автоматически
        return {"slug": ("title",)}