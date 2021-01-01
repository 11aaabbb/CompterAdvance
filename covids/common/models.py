from django.db import models

# Create your models here.
class allStates(models.Model):
    province = models.CharField(default="NY", max_length=50)
    Update = models.CharField(default="1/1/1970", max_length=50)
    confirmed  = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    active = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    updateTime = models.DateTimeField(auto_now_add=True)

class timeSeriseConfirmed(models.Model):
    uid = models.CharField(primary_key=True,default="8000000", max_length=50)
    city = models.CharField(default="NYC", max_length=50)
    province = models.CharField(default="NY", max_length=50)
    cityName = models.CharField(default=None, max_length=50)
    confirmed = models.CharField(default=None, max_length=5000)
    Range = models.CharField(default=None, max_length=5000)


class timeSeriseDeath(models.Model):
    uid = models.CharField(primary_key=True, default="8000000", max_length=50)
    city = models.CharField(default="NYC", max_length=50)
    province = models.CharField(default="NY", max_length=50)
    cityName = models.CharField(default=None, max_length=50)
    death = models.CharField(default=None, max_length=5000)
    Range = models.CharField(default=None, max_length=5000)

