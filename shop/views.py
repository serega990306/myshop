from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product, Top_Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
# Страница с товарами


def register(request):
    content = {}
    if request.user.is_authenticated:
        content = {'username': auth.get_user(request).username}
        username = content['username']
        s = username[0] + username[1]
        s = s.upper()
        content['letters'] = s
        return redirect('/profile', content)
    content.update(csrf(request))
    content['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            username = request.POST.get('username', '')
            password = request.POST.get('password1', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                s = username[0] + username[1]
                s = s.upper()
                content['letters'] = s
                auth.login(request, user)
                return redirect('/profile', content)
            else:
                content['form'] = newuser_form
        else:
            content['reg_error'] = 'Пароль должен быть более 8 символов и состоять из букв и цифр'
    return render_to_response('registration.html', content)


def login(request):
    content = {}
    content.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            content['username'] = username
            auth.login(request, user)
            return redirect('/profile', content)
        else:
            content['login_error'] = 'Пользователь не найден'
            return render_to_response('login.html', content)
    else:
        return render_to_response('login.html', content)


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    content = {}
    user = auth.get_user(request).id

    if request.user.is_authenticated:
        content = {'username': auth.get_user(request).username}
        return render(request, 'profile.html', content)
    else:
        return redirect('/', content)


def ProductList(request, category_slug=None, page_number=1):
    content = {}
    category = None
    top = Top_Product.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    current_page = Paginator(products, 30)
    content['category'] = category
    content['categories'] = categories
    #content['products'] = products
    content['products'] = current_page.page(page_number)
    content['top_products'] = top
    content['category_slug'] = category_slug
    return render(request, 'product/list.html', content)


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render_to_response('product/detail.html',
                             {'product': product,
                              'cart_product_form': cart_product_form})
