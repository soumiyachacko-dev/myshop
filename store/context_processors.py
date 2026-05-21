from .models import Category, Product

def menu_data(request):
    data = []
    categories = Category.objects.all()
    for cat in categories:
        products = Product.objects.filter(category=cat)
        data.append({'category': cat, 'products': products})
    return {'menu_data': data}