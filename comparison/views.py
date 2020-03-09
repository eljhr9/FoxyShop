from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .comparison import Compare

@require_POST
def compare_add(request, product_id):
    compare = Compare(request)
    comp = request.session.get('compare')
    compare_items = Product.objects.filter(id__in=comp)

    product = get_object_or_404(Product, id=product_id)
    if compare.availability(product):
        return redirect('compare:compare_remove', product_id)
    if compare_items.count() >= 4:
        return redirect('index')
    compare.add(product=product)
    if 'products' in request.POST:
        return redirect('shop:products')
    elif 'product' in request.POST:
        return redirect(product.get_absolute_url())
    else:
        return redirect('compare:compare_detail')

def compare_remove(request, product_id):
    compare = Compare(request)
    product = get_object_or_404(Product, id=product_id)
    compare.remove(product)
    # return redirect('compare:compare_detail')
    return redirect('shop:products')

def compare_detail(request):
    return render(request, 'comparison/detail.html', {})
