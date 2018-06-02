from django.conf.urls import url, include
from . import views
from django.views.generic import TemplateView

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.OrderCreate, name='OrderCreate'),
    url(r'^fail-payment/$', TemplateView.as_view(template_name='fail.html'), name='payment_fail'),
    url(r'^success-payment/$', TemplateView.as_view(template_name='success.html'), name='payment_success'),
    url(r'^yandex-money/', include('yandex_money.urls')),
]
