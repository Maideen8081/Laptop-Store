from django.contrib import admin
from .models import Account,UserProfile
from django.utils.html import format_html





# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self,object):
#         #return format_html('<img src="{}" width="30",style="border-radius:50%"; >'.format(object.profile_picture.url))
#     #thumbnail.short_description='profile picture'
#         list_display=('user','city','state','country')
    
admin.site.register(Account)
admin.site.register(UserProfile)

# Register your models here.
