from django.conf.urls import url
from products.views import (ProductListView,
                            # product_list_view,
                            # ProductDetailView,
                            # product_detail_view,
                            # ProductFeaturedListView,
                            # ProductFeaturedDetailView,
                            ProductDetailSlugView,)
app_name='products'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='detail'),
    url(r'^$',ProductListView.as_view(),name='list'),

]
