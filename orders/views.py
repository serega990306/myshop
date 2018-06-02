from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Profile
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic import TemplateView
from yandex_money.forms import PaymentForm
from yandex_money.models import Payment


def get_context_data(ctx, number):
    payment = Payment(order_amount=number)
    payment.save()

    ctx['form'] = PaymentForm(instance=payment)
    return ctx


def OrderCreate(request):
    email = ''
    content = {}
    cart = Cart(request)
    user = auth.get_user(request).id
    user_info = User.objects.filter(id=user).all()
    for e in user_info:
        email = e.username
    info = Profile.objects.filter(user_id=user).all()
    for e in info:
        name = e.name
        content['name'] = e.name
        surname = e.surname
        country = e.country
        state = e.state
        city = e.city
        street = e.street
        home = e.home
        appartment = e.appartment
        index = e.index
        phone_number = e.phone_number
    content['cart'] = cart
    content['username'] = auth.get_user(request).username
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            order = form.save(commit=False)
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            total_price = Order.get_total_cost(self=order)
            cart.clear()
            content['order'] = order

            item = Order.objects.filter(email=email).all()[:1]
            for e in item:
                number = str(e.id)

            get_context_data(content, total_price)

            stri = 'Спасибо за ваш заказ на сумму: ' + str(total_price) + '\nНомер вашего заказа: ' + str(number)
            try:
                send_mail(
                    'Заказ на BeautyFace',
                    stri,
                    'service@kcosmetic.ru',
                    [email],
                    fail_silently=False,
                )
            except:
                print('Письмо не отправлено')
            return render(request, 'order/pay_for_order.html', content)
    if request.user.is_authenticated:
        form = OrderCreateForm(initial={'email': email, 'first_name': name, 'last_name': surname, 'country': country, 'state': state,
                                    'city': city, 'street': street, 'home': home, 'appartment': appartment,
                                    'index': index, 'phone_number': phone_number})
    else:
        form = OrderCreateForm()
    content['form'] = form
    return render(request, 'order/create.html', content)
