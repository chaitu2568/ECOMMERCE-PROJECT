from django.shortcuts import render, get_object_or_404
from .models import Product
from django.views.generic import ListView,DetailView
from django.http import Http404
# Create your views here.
class ProductFeaturedListView(ListView):
    # queryset=Product.objects.all()
    template_name='products/lists.html'

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    queryset=Product.objects.all().featured()
    template_name='products/featured-detail.html'
    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     return Product.objects.featured()


class ProductListView(ListView):
    # queryset=Product.objects.all()
    template_name='products/lists.html'

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()


def product_list_view(request):
    queryset=Product.objects.all()
    context={'object_list':queryset}
    return render(request,'products/lists.html',context)

class ProductDetailSlugView(DetailView):
    queryset=Product.objects.all()
    template_name='products/detail.html'
    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        # instance=Product.objects.get_object_or_404(Product,slug=slug,active=True)
        try:
            instance=Product.objects.get(slug=slug,active=True)
        except Product.DoesNotExist:
            raise Http404('No Product with that slug')
        except Product.MultipleObjectsReturned:
            qs=Product.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404('Naavalla Kaadu')

        return instance


class ProductDetailView(DetailView):
    # queryset=Product.objects.all()
    template_name='products/detail.html'

    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        return context

    def get_object(self,*args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        instance=Product.objects.get_by_id(pk)

        if instance is None:
            raise Http404('Product doesnt exist')
        return instance

    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     pk=self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)





def product_detail_view(request,pk=None,*args,**kwargs):
    # instance=get_object_or_404(Product,pk=pk)
    # queryset=Product.objects.get(pk=pk)
    instance=Product.objects.get_by_id(pk)

    if instance is None:
        raise Http404('Product doesnt exist')

    # qs=Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() ==1:
    #     instance=qs.first()
    # else:
    #     raise Http404('Product doesnt exist')



    context={'object':instance}
    return render(request,'products/detail.html',context)
