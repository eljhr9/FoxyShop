"""django_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from shop.urls import views
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap
from blog.sitemaps import BlogSitemap
from django.conf.urls.i18n import i18n_patterns


sitemaps = {
    'products': ProductSitemap,
    'articles': BlogSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('payment/', include('payment.urls')),
    path('comparison/', include('comparison.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('collection/', include('shop.urls')),
    path('account/', include('users.urls')),
    path('empty/', views.empty, name='empty'),
    path('blog/', include('blog.urls')),
    path('coupons/', include('coupons.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)
