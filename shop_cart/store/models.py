from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg

class Products(models.Model):
   
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    product_name = models.CharField(max_length=100,null=False)
    slug=models.SlugField(max_length=100,unique=True)
    product_image = models.ImageField(upload_to='photos/products',null=False)
    price=models.IntegerField(null=False,blank=False)
    description = models.CharField(max_length=500,null=False,blank=False)
    stock = models.IntegerField(null=False,blank=False)
    is_available=models.BooleanField(default=True)
    create_date=models.DateTimeField(auto_now_add=True)
    modifie_dated=models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])
    
    
    def __str__(self):
        return self.product_name 
    
    def averageReview(self):
        revies=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if revies['average'] is not None:
            avg=float(revies['average'])
        return avg    
    
    
    
    
class variationmanager(models.Manager):
    def Colors(self):
        return super(variationmanager,self).filter(variation_category='Color',is_active=True)
    
    
    def Sizes(self):
        return super(variationmanager,self).filter(variation_category='Size',is_active=True)
    
    def RAMs(self):
        return super(variationmanager,self).filter(variation_category='RAM',is_active=True)
    
    def Processors(self):
        return super(variationmanager,self).filter(variation_category='Processor',is_active=True)
    
        
    
    
variation_category=(
      
      ('Color','Color'),
      ('RAM','RAM'),
      ('Processor','Processor'),
      ('Size','Size'),
  )
class Variation(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)  
    variation_category=models.CharField(max_length=100,choices=variation_category) 
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    
    objects=variationmanager()
    
    
    
    
    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True,null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.subject
    
    

# Create your models here.
