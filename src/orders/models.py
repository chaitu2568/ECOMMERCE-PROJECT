from django.db import models
from carts.models import Cart
from Ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save,post_save
import math

ORDER_STATUS_CHOICES=(('created','Created'),('paid','Paid'),('shipped','Shipped'),('refunded','Refunded'))
# Create your models here.
class Order(models.Model):
    order_id=models.CharField(max_length=120,blank=True)
    # billinig prof
    # shipping add
    # shippingprof
    cart=models.ForeignKey(Cart,on_delete='CASCADE')
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total=models.DecimalField(decimal_places=2,max_digits=100,default=6.85)
    total=models.DecimalField(decimal_places=2,max_digits=100,default=0.00)


    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        add_total=math.fsum([cart_total,shipping_total])
        format_total=format(add_total,'.2f')
        self.total=format_total
        self.save()
        return format_total

def pre_save_random_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
pre_save.connect(pre_save_random_order_id,sender=Order)


def post_save_order_tocart(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_id=cart_obj.id
        cart_total=cart_obj.total
        qs=Order.objects.filter(cart__id=cart_id)
        if qs.count==1:
            order_obj=qs.first()
            order_obj.update_total()

post_save.connect(post_save_order_tocart,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)
