from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True, null=True,blank=True)
    category_image = models.ImageField( upload_to='photos/categories',null=True,blank=True)
    category_description = models.TextField(max_length=500,null=False,blank=False)
    
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
        
    def get_url(self):
        return reverse('products_by_category',args=[self.slug]) 
    
     
    def __str__(self):
        return self.category_name
