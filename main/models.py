from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin


class User(AbstractUser):
    is_operational = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)



class Operational(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=10)
    file = models.FileField(blank=True, null=True)
    # file = models.FileField(upload_to='tag/', blank=True, null=True)



# User._meta.get_field('email')._unique = True
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False



# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


admin.site.register(User)
admin.site.register(Operational)
# admin.site.register(Client)
