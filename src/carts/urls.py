from django.conf.urls import url
from .views import (cart_home,
                    cart_update,check_out,check_out_complete_view)
app_name='carts'
urlpatterns = [
    url(r'^success/$',check_out_complete_view,name='success'),
    url(r'^check_out/$',check_out,name='checkout'),
    url(r'^update/$',cart_update,name='update'),
    url(r'^$',cart_home,name='home'),
]
