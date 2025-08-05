from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class profile(models.Model):
    
    user=models.OneToOneField(User , related_name='profile' ,on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50 , default="" , blank=True)
    reset_password_expire = models.DateTimeField(null=True , blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    
    # def __str__(self):
    #     return self.user.username
    def __str__(self):
        return f"ملف {self.user.username}"
    
@receiver(post_save , sender=User)
def save_profile(sender , instance , created ,**kwargs):
    print('instance',instance)
    user= instance
    if created:
        the_profile=profile(user=user)
        the_profile.save()
    
    
    
    