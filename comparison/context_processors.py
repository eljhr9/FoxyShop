from shop.models import Product

def compare(request):
    comp = request.session.get('compare')
    try:
        compare_items = Product.objects.filter(id__in=comp)
    except:
        # compare_items = Product.objects.get(id=1)
        compare_items = None
    return {'compare': compare_items, 'compare_items': compare_items}
