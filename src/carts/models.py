from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save,post_save,m2m_changed
from decimal import Decimal
# Create your models here.
User=settings.AUTH_USER_MODEL

class CartManager(models.Manager):

    def get_or_new(self,request):
        cart_id=request.session.get('cart_id',None)
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            obj_new=False
            print('Cart Exists')
            print(cart_id)
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
        else:
            obj_new=True
            cart_obj=Cart.objects.new(user=request.user)
            request.session['cart_id']=cart_obj.id
        return cart_obj, obj_new

    def new(self,user=None):
        print(user)
        user_obj=None
        if user is not None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete='CASCADE')
    products=models.ManyToManyField(Product, blank=True)
    subtotal=models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total=models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=CartManager()
    def __str__(self):
        return str(self.id)

# This function is called whenever we changed the products in the cart. And
# returns the final price of all producs present in carts

def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action=='post_add' or action=='post_remove' or action=='post_clear':
        products=instance.products.all()
        total=0
        for product in products:
            total+=product.price
        if instance.subtotal!=total:
            instance.subtotal=total
            instance.save()

# Signals
m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)


def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    if instance.subtotal>0:
        instance.total=Decimal(instance.subtotal) + Decimal(10)
    else:
        instance.total=0

pre_save.connect(pre_save_cart_receiver,sender=Cart)
