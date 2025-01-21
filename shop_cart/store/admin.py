from django.contrib import admin
from .models import Products,Variation,ReviewRating


class CategoryAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','modifie_dated','category','is_available')

    prepopulated_fields={'slug':('product_name',)}
    
    
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active','created_date')   
    list_editable=('is_active',) 
    list_filter=('product','variation_category','variation_value','created_date')
   

admin.site.register(Products,CategoryAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
