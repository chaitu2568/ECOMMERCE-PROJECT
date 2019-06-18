from django.conf.urls import url
from products.views import (ProductListView,
                            # product_list_view,
                            # ProductDetailView,
                            # product_detail_view,
                            # ProductFeaturedListView,
                            # ProductFeaturedDetailView,
                            ProductDetailSlugView,)

urlpatterns = [

    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view()),
    url(r'^$',ProductListView.as_view()),

]
