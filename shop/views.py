from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product, Top_Product, Brand
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.core.mail import send_mail
from .models import Profile, Variation
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
            name = request.POST.get('name', '')
            surname = request.POST.get('surname', '')
            str = 'Спасибо за регистрацию!\nВаш логин: ' + username + '\nВаш пароль: ' + password
            try:
                send_mail(
                    'Регистрация на BeautyFace',
                    str,
                    'service@kcosmetic.ru',
                    [username],
                    fail_silently=False,
                )
            except:
                print('Письмо не отправлено')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                Profile.objects.create(name=name, surname=surname, user=user)
                s = username[0] + username[1]
                s = s.upper()
                content['letters'] = s
                auth.login(request, user)
                return redirect('/profile', content)
            else:
                content['form'] = newuser_form
        else:
            content['reg_error'] = 'Пароль должен быть более 8 символов и состоять из букв и цифр'
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                content['reg_error'] = 'Введенные пароли не совпадают'
            if User.objects.filter(username=username).exists():
                content['reg_error'] = 'Пользователь с таким логином уже существует'
    return render_to_response('registration.html', content)


def login(request):
    content = {}
    content.update(csrf(request))
    if request.user.is_authenticated:
        content = {'username': auth.get_user(request).username}
        username = content['username']
        s = username[0] + username[1]
        s = s.upper()
        content['letters'] = s
        return redirect('/profile', content)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            content['username'] = username
            auth.login(request, user)
            return redirect('/profile', content)
        else:
            content['login_error'] = 'Имя пользователя или пароль введены неверно'
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
        if request.POST:
            name = request.POST.get('name', '')
            surname = request.POST.get('surname', '')
            country = request.POST.get('country', '')
            state = request.POST.get('state', '')
            city = request.POST.get('city', '')
            street = request.POST.get('street', '')
            home = request.POST.get('home', '')
            appartment = request.POST.get('appartment', '')
            index = request.POST.get('index', '')
            phone_number = request.POST.get('phone_number', '')
            Profile.objects.filter(user_id=user).update(name=name, surname=surname, country=country, state=state, city=city,
                                             street=street, home=home, appartment=appartment, index=index,
                                             phone_number=phone_number)
        info = Profile.objects.filter(user_id=user).all()
        for e in info:
            content['name'] = e.name
            content['surname'] = e.surname
            content['country'] = e.country
            content['state'] = e.state
            content['city'] = e.city
            content['street'] = e.street
            content['home'] = e.home
            content['appartment'] = e.appartment
            content['index'] = e.index
            content['phone_number'] = e.phone_number
        return render(request, 'profile.html', content)
    else:
        return redirect('/', content)


def connect(request):
    content = {}
    content.update(csrf(request))
    if request.user.is_authenticated:
        content = {'username': auth.get_user(request).username}
        user = auth.get_user(request).id
        info = Profile.objects.filter(user_id=user).all()
        for e in info:
            content['name'] = e.name
    if request.POST:
        username = request.POST.get('username', '')
        text = request.POST.get('text', '')
        str = 'Письмо от: ' + username + '\n' + text
        try:
            send_mail(
                'Письмо со страницы связи',
                str,
                'studiovagiton@yandex.ru',
                [username],
                fail_silently=False,
            )
        except:
            print('Письмо не отправлено')
        content['answer'] = 'Спасибо за ваше письмо!'
    return render(request, 'connect.html', content)


def help(request):
    content = {}
    content.update(csrf(request))
    return render(request, 'help.html', content)


def mail(request):
    content = {}
    content.update(csrf(request))
    return render(request, 'fd4b3799b6bb.html', content)


def ProductList(request, category_slug=None, brand_category_slug=None, page_number=1):
    content = {}
    category = None
    brand = None
    products = None
    top1 = Top_Product.objects.all()[:4]
    top2 = Top_Product.objects.all()[4:]
    if not request.POST:
        products = Product.objects.filter(available=True)
    if request.POST:
        sort = request.POST.get('sort', '')
        if sort == 'По возрастанию цены':
            products = Product.objects.filter(available=True).order_by('price')
        if sort == 'По убыванию цены':
            products = Product.objects.filter(available=True).order_by('-price')
        if sort == 'Новинки':
            products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if brand_category_slug:
        brand = get_object_or_404(Brand, slug=brand_category_slug)
        products = products.filter(brand=brand)
    current_page = Paginator(products, 40)
    content['category'] = category
    content['products'] = current_page.page(page_number)
    content['top_products'] = top1
    content['top_products2'] = top2
    content['category_slug'] = category_slug
    content['brand_category_slug'] = brand_category_slug
    content['brand'] = brand
    return render(request, 'product/list.html', content)


def ProductDetail(request, id, slug):
    content = {}
    stock = []
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    variations = Variation.objects.filter(product=product).all()
    cart_product_form = CartAddProductForm()

    for e in range(1, product.stock + 1):
        stock.append(e)
    content['product'] = product
    content['variations'] = variations
    content['stock'] = stock
    content['cart_product_form'] = cart_product_form
    return render(request, 'product/detail.html', content)

