from django.conf.urls import url
from . import views

app_name = 'cupon'

urlpatterns = [
    url(r'^apply', views.CuponApply, name='apply')
]