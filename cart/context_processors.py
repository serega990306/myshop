from .cart import Cart
from shop.models import Brand, Category
from django.contrib import auth
from shop.models import Profile


def cart(request):
    content = {}

    if request.user.is_authenticated:
        content['username'] = auth.get_user(request).username
        user = auth.get_user(request).id
        info = Profile.objects.filter(user_id=user).all()
        for e in info:
            content['name'] = e.name

    content['cart'] = Cart(request)
    content['brands'] = Brand.objects.all()
    content['categories'] = Category.objects.all()
    return content
