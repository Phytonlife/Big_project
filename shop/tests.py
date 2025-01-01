from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy


class ProductViewTest(TestCase):#Тестирование продуктов
    def test_get_products(self):#Получение продуктов с помощью шаблона products
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )#Создание изображения с помощью библиотеки Pillow и библиотеки SimpleUploadedFile для того чтобы сохранить его в базе данных в виде бинарного файла в виде бинарного файла

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')#Создание продукта с помощью модели Product и создание категории с помощью модели Category и сохранение изображения в базе данных
        category = Category.objects.create(name='django')#Создание категории с помощью модели Category и сохранение изображения в базе данных
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')#Создание продукта с помощью модели Product и сохранение изображения в базе данных
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')#Создание продукта с помощью модели Product и сохранение изображения в базе данных

        response = self.client.get(reverse('shop:products'))#Получение продуктов с помощью шаблона products

        self.assertEqual(response.status_code, 200)#Проверка статуса ответа
        self.assertEqual(response.context['products'].count(), 2)#Проверка количества продуктов
        self.assertEqual(list(response.context['products']), [product_1, product_2])#Проверка списка продуктов
        self.assertContains(response, product_1)#Проверка наличия продукта в списке
        self.assertContains(response, product_2)#Проверка наличия продукта в списке


class ProductDetailViewTest(TestCase):#Тестирование продуктов
    def test_get_product_by_slug(self):#Получение продуктов с помощью шаблона product_detail с использованием slug продукта
        # Create a product
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )# Create an image for the product using Pillow and SimpleUploadedFile
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')# Create a category and product and save the image to the database
        category = Category.objects.create(name='Category 1')# Create a product and save the image to the database
        product = Product.objects.create(
            title='Product 1', category=category, slug='product-1', image=uploaded)# Make a request to the product detail view with the product's slug
        # Make a request to the product detail view with the product's slug
        response = self.client.get(
            reverse('shop:product-detail', kwargs={'slug': 'product-1'}))

        # Check that the response is a success
        self.assertEqual(response.status_code, 200)

        # Check that the product is in the response context
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_status_code(self):
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)