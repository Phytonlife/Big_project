import random
import string
from django.urls import reverse
from django.db import models
from django.utils.text import slugify   #Нужно чтобы создавались уникальные слаги
# Create your models here.


def rand_slug():#Создание уникального слага
    return "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(3))

class Category(models.Model):
    name = models.CharField(max_length=250,db_index=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    slug = models.SlugField("URL",max_length=250,unique=True,db_index=True,null=True,editable=True)
    created_at = models.DateTimeField("Дата создание",auto_now_add=True)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        full_path = [self.name]
        k=self.parent
        while k is not None:
            full_path.append(k.name)
            k=k.parent
        return ' -> '.join(full_path[::-1])
    def save(self, *args, **kwargs):  #Создание уникального слага
        if not self.slug:
            self.slug = slugify(rand_slug()+"-pickBetter"+self.name)   #Нужно чтобы создавались уникальные слаги
        super(Category, self).save(*args, **kwargs)#Сохранение слага в базе данных вызов метода save из models.Model




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    title=models.CharField("Название",max_length=250)
    brand=models.CharField("Бренд",max_length=250)
    description=models.TextField("Описание",blank=True)
    slug = models.SlugField("URL",max_length=250)
    price=models.DecimalField("Цена",max_digits=10,decimal_places=2,default=99.99)
    image=models.ImageField("Изображение",upload_to="products/%Y/%m/%d",blank=True)
    aviable=models.BooleanField("В наличии",default=True)
    created_at = models.DateTimeField("Дата создание",auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновление",auto_now=True)

    class Meta:
        verbose_name='Товар'
        verbose_name_plural="Товары"

    def __str__(self):
        return self.title

class ProductManager(models.Manager): #Менеджер для отображения только активных продуктов в админке
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(aviable=True)

class ProductProxy(Product):#Прокси модели для отображения только активных продуктов в админке
    objects = ProductManager()
    class Meta:
        proxy = True
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"