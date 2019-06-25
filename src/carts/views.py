from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from orders.models import Order
# Create your views here.

def cart_home(request):
    cart_obj,obj_new=Cart.objects.get_or_new(request)
    return render(request,'carts/home.html',{'cart':cart_obj})

def cart_update(request):
    product_id=request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product Not Present right Now")
            return redirect('carts:home')
        cart_obj,obj_new=Cart.objects.get_or_new(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_id)
        else:
            cart_obj.products.add(product_id)
        request.session['cart_list']=cart_obj.products.count()
    return redirect('carts:home')

def check_out(request):
    cart_obj,obj_new=Cart.objects.get_or_new(request)
    order_obj=None
    if obj_new or cart_obj.products.count()==0:
        return redirect('carts:home')
    else:
        order_obj,ord_new=Order.objects.get_or_create(cart=cart_obj)
    return render(request,'carts/check_out.html',{'object':order_obj})
