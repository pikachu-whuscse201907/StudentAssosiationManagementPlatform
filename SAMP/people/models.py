from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    pswd = models.CharField(max_length=256)
    cookie_id = models.CharField(max_length=256,null=True)
    cookie_create_time = models.DateTimeField(blank=True,null=True)
    cookie_expire=models.DateTimeField(blank=True,null=True)
