from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse
from django.conf import settings
# Create your views here.


import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_cu1lQmcg1OLffhLvYrSCp5XE")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_PrV61avxnHaWIYZEeiYTTVMZ')
stripe.api_key = STRIPE_SECRET_KEY

def cart_detail_api_view(request):
    cart_obj,obj_new=Cart.objects.get_or_new(request)
    products= [{'name':i.title,
    'price':i.price,
    'url':i.get_absolute_url(),
    'id':i.id} for i in cart_obj.products.all()]
    cart_data={'products':products,'subtotal':cart_obj.subtotal,'total':cart_obj.total}
    return JsonResponse(cart_data)


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
            added=False
        else:
            cart_obj.products.add(product_id)
            added=True
        request.session['cart_list']=cart_obj.products.count()
        if request.is_ajax():
            json_data={
            'added':added,
            'removed':not added,
            'cartUpdateCount':cart_obj.products.count()
            }
            return JsonResponse(json_data,status=200)
            # return JsonResponse({'message':'Error 400'},status_code=400)
    return redirect('carts:home')

def check_out(request):
    cart_obj,obj_new=Cart.objects.get_or_new(request)
    order_obj=None
    if obj_new or cart_obj.products.count()==0:
        return redirect('carts:home')
    login_form=LoginForm()
    guest_form=GuestForm()
    address_form=AddressForm()
    shipping_address_id=request.session.get('shipping_address_id',None)
    billing_address_id=request.session.get('billing_address_id',None)
    billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
    address_qs=None
    has_card=False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs=Address.objects.filter(billing_profile=billing_profile)
        order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address=Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
        has_card=billing_profile.has_card

    if request.method=='POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_done()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("carts:success")
            else:
                print(crg_msg)
                return redirect("carts:checkout")

    context={'object':order_obj,'billing_profile':billing_profile,
    'login_form':login_form,
    'guest_form':guest_form,
    'address_form':address_form,
    'address_qs':address_qs,
    'has_card':has_card,
    'publish_key':STRIPE_PUB_KEY,
    }
    # 'billing_address_form':billing_address_form}
    return render(request,'carts/check_out.html',context)


def check_out_complete_view(request):
    return render(request,'carts/checkout_success.html',{})
