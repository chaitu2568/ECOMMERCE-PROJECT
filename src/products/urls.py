from django.conf.urls import url
from products.views import (ProductListView,
                            ProductDetailSlugView,)
app_name='products'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='detail'),
    url(r'^$',ProductListView.as_view(),name='list'),

]
