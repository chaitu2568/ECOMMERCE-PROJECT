from django.db import models
import random
import os
from .utils import unique_slug_generator
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.db.models import Q


def divide_filename_ext(filepath):
    basename=os.path.basename(filepath)
    # divide the file name and extension
    name,ext=os.path.splitext(basename)
    return name,ext

def upload_image_path(instance,filename):
    new_filename=random.randint(1,3455958959)
    name,ext=divide_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(new_filename=new_filename,final_filename=final_filename)


# Create your models here.
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True,active=True)

    def search(self,query):
        lookups=Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def features(self):
        return self.get_queryset().featured()

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id) #get.queryset()==Product.objects
        if qs.count()==1:
            return qs.first()
        else:
            return None
    def search(self,query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(blank=True,unique=True)
    description=models.TextField()
    price=models.DecimalField(decimal_places=3,max_digits=20,default=48.333)
    image=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=ProductManager()
    def get_absolute_url(self):
        # return '/products/{slug}'.format(slug=self.slug)
        return reverse('products:detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

# To give a slug a random value before it saves in database
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender=Product)
