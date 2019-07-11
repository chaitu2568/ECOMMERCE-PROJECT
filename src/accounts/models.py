from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self,email,full_name=None,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Please enter an valid email ID')
        if not password:
            raise ValueError('Users must have an Password')
        # if not full_name:
        #     raise ValueError('User Must have to give their full_name')

        user_obj=self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.active=is_active
        user_obj.admin=is_admin
        user_obj.staff=is_staff
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,full_name=None,password=None):
        user=self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self,email,full_name=None,password=None):
        user=self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    full_name=models.CharField(max_length=255,blank=True,null=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    timestamp=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects=UserManager()

    def get_full_name(self):
        if self.full_name:
            return full_name
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

# All the below functions are get from the documentation to get the user Permissions
    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

# Create your models here.
class GuestEmail(models.Model):
    Email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Email
