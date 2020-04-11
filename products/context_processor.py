from .models import Category, Product


def categories(request):
    all_cats = Category.objects.all()
    return {'all_categories': all_cats}


def all_products(request):
    all_products = Product.objects.order_by('created_at')
    return {'all_products': all_products}


def cities(request):
    all_city = Product.objects.order_by(
        'city').values_list('city', flat=True).distinct()
    return {'all_city': all_city}


def areas(request):
    all_area = Product.objects.order_by(
        'area').values_list('area', flat=True).distinct()
    return {'all_area': all_area}
