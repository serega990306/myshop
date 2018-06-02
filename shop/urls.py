from django.conf.urls import url, include
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),
    path('fd4b3799b6bb.html/', views.mail, name='mail'),
    path('help/', views.help, name='help'),
    path('connect/', views.connect, name='connect'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    url(r'^page/(?P<page_number>\d+)/$', views.ProductList, name='ProductList'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^category/(?P<category_slug>[-\w]+)/page/(?P<page_number>\d+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^brand/(?P<brand_category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^brand/(?P<brand_category_slug>[-\w]+)/page/(?P<page_number>\d+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
