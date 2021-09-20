from django.db import models

# Create your models here.
class Stock(models.Model):
    sector = models.CharField(max_length=50,blank=True,null=True)
    industry = models.CharField(max_length=50,blank=True,null=True)
    updatedTime = models.CharField(max_length=50,blank=True,null=True)
    recentQuarter = models.IntegerField(blank=True,null=True)
    symbol = models.CharField(max_length=10,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    ipoyear= models.CharField(max_length=10,blank=True,null=True)
    fullName = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.symbol