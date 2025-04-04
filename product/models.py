from django.db import models as m
from django.contrib.auth.models  import User

# Create your models here.

class  Category(m.TextChoices):
    COMPUTERS="COMPUTERS"
    FOOD="FOOD"
    KIDS="KIDS"
    HOME="HOME"
class  Product(m.Model):
    name=m.CharField(default="",max_length=200,blank=False)
    description=m.TextField(default="",max_length=1000,blank=True)
    price=m.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand=m.CharField(default="",max_length=200,blank=False)
    category=m.CharField(max_length=40,blank=False,choices=Category.choices)
    ratings=m.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock=m.IntegerField(default=0)
    createAt=m.DateTimeField(auto_now_add=True)
    image=m.ImageField(upload_to="photo/%y/%m/%d",blank=True,null=True)
    user=m.ForeignKey(User,on_delete=m.SET_NULL,null=True)
    
    def __str__(self):
        return self.name
    