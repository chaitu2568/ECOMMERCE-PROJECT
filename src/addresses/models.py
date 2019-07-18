from django.db import models
from billing.models import BillingProfile

# Create your models here.

ADDRESS_TYPES=(
        ('billing','Billing'),
        ('shipping','Shipping'),
)
class Address(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type=models.CharField(max_length=120,choices=ADDRESS_TYPES)
    address_line_1=models.CharField(max_length=120)
    address_line_2=models.CharField(max_length=120,null=True,blank=True)
    city=models.CharField(max_length=120)
    country=models.CharField(max_length=120,default='INDIA')
    state=models.CharField(max_length=120)
    postal_code=models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def pulladdress(self):
        return "{add1}\n{add2}\n{city}\n{country}\n{state}\n{postal_code}\n".format(
        add1=self.address_line_1,
        add2=self.address_line_2 or "",
        city=self.city,
        country=self.country,
        state=self.state,
        postal_code=self.postal_code

        )
