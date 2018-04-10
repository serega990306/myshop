from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product, Top_Product
from cart.forms import CartAddProductForm
# Страница с товарами


def ProductList(request, category_slug=None):
    content = {}
    category = None
    top = Top_Product.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    content['category'] = category
    content['categories'] = categories
    content['products'] = products
    content['top_products'] = top
    return render(request, 'product/list.html', content)


def ProductListByBrand(request, category_slug=None):
    '''
    brand = None
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    print(brands)
    if category_slug:
        brand = get_object_or_404(Brand, slug=category_slug)
        products = products.filter(category=brand)
    return render(request, 'product/list.html', {
        'brand': brand,
        'brands': brands,
        'products': products
    })'''


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render_to_response('product/detail.html',
                             {'product': product,
                              'cart_product_form': cart_product_form})
