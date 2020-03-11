from shop.models import Product

def compare(request):
    comp = request.session.get('compare')
    compare_items = Product.objects.filter(id__in=comp)
    return {'compare': compare_items, 'compare_items': compare_items}
