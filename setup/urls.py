"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('about/', views.about, name='about-us'),
    path('contact/', views.contact, name='contact-us'),
    path('faqs/', views.faqs, name='faqs'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('loutout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('store/<str:name>/', views.store, name='store'),
    path('checkout/<str:name>/', views.checkout, name='checkout'),
    path('update-cart/', views.updateCart, name='update-cart'),
    path('process-order/', views.processOrder, name='process-order'),
    path('delete-order/', views.deleteOrder, name='delete-order'),
    path('profile/overview/', views.profileOverview, name='profile-overview'),
    path('profile/order/', views.profileOrder, name='profile-order'),
    path('profile/voucher/', views.profileVoucher, name='profile-voucher'),
    path('profile/favourite/', views.profileFavourite, name='profile-favourite'),
    path('profile/vendor/', views.profileVendor, name='profile-vendor'),
    path('merchant/register/', views.registerVendor, name='register-vendor'),
    path('delete-vendor/', views.deleteVendor, name='delete-order'),
    path('query-google-map/', views.queryGoogleMap, name='query-google-map')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
