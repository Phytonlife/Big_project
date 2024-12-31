from .models import Category


def categories(request):
    categories=Category.objects.filter(parent=None) #Выводим только родительские категории у которых нет parent
    return {'categories':categories}
