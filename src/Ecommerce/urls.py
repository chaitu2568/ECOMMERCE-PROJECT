"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from accounts.views import LoginView,RegisterView
from .views import home_page,contact_page,about_page
from accounts.views import guest_register_page
from addresses.views import check_out_address_create_view,check_out_address_reuse_view
from carts.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_createview
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView

urlpatterns = [

    url(r'^bootstrap/$',TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^search/',include('search.urls',namespace='search')),
    url(r'^products/',include('products.urls',namespace='products')),
    url(r'^carts/',include('carts.urls',namespace='carts')),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^billing/payment_method/$',payment_method_view,name='billing_payment_method'),
    url(r'^billing/payment_method/create/$',payment_method_createview,name='billing_payment_method_endpoint'),
    url(r'^check_out/address/reuse_view/$',check_out_address_reuse_view,name='check_out_address_reuse'),
    url(r'^check_out/address/create_view/$',check_out_address_create_view,name='check_out_address_create_view'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^api/cart/$',cart_detail_api_view,name='cart-api'),
    url(r'^register/guest/$',guest_register_page,name='guest_register'),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    url(r'^login/$',LoginView.as_view(),name='login'),
	url(r'^contact/$',contact_page,name='contact'),
	url(r'^about/$',about_page,name='about'),
	url(r'^$',home_page,name='home'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns=urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns=urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
