from .comparison import Compare
from shop.models import Product

def compare(request):
    compare = Compare(request)
    comp = request.session.get('compare')
    compare_items = Product.objects.filter(id__in=comp)
    return {'compare': compare, 'compare_items': compare_items}
