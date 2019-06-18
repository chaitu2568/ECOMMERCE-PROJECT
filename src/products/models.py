from django.db import models
import random
import os

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


class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(blank=True,unique=True)
    description=models.TextField()
    price=models.DecimalField(decimal_places=3,max_digits=20,default=48.333)
    image=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    objects=ProductManager()


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title