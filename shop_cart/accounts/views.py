from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from.forms import RegistratioForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from orders.models import Order 
from django.contrib import messages
from django.contrib import messages,auth
from store.models import Products
from django.contrib.auth.decorators import login_required
#verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.views import _cart_id
from cart.models import Cart,CartItems
def register(request):
    
    if request.method =='POST':
        form=RegistratioForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
           # is_active=form.cleaned_data[' is_active']
            
            user =Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.is_active=True
            user.save()
            
            #User Activation
            
            # current_site=get_current_site(request)
            # mail_subject ='pleace Activate Your Account'
            # message=render_to_string('accounts/account_verification_mail.html',{
            #     'user':user,
            #     'domain':current_site,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':default_token_generator.make_token(user),
            # })
            
            # to_email=email
            # send_email=EmailMessage(mail_subject,message,to=[to_email])
            # send_email.send()
            
            messages.success(request,'regidtration Successfull')
            return redirect('register')
            
            
    else:
            form=RegistratioForm()
    contex={
               'form':form,
            }
    return render(request,'accounts/register.html',contex)


def login(request):
    if request.method =='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user = auth.authenticate(email=email,password=password)
        
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItems.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItems.objects.filter(cart=cart)
                    
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))
                        
                        cart_item=CartItems.objects.filter(user=user)
        
                        ex_var_list=[]
                        id=[]
                        for item in cart_item:
                           existing_variation=item.variations.all()
                           ex_var_list.append(list(existing_variation))
                           id.append(item.id)
                           
                           
                           
                        for pr in product_variation:
                            if pr in ex_var_list:
                                index=ex_var_list.index(pr)
                                item_id=id[index]
                                item-CartItems.objects.get(id=item_id)
                                item.quantity+=1
                                item.user=user
                                item.save()   
                            else:
                                cart_item=CartItems.objects.filter(cart=cart) 
                                for item in cart_item :  
                                   item.user=user
                                   item.save()
            except:
                pass    
            auth.login(request,user)
            messages.success(request,'regidtration Successfull')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    
    return render(request,'accounts/login.html')

@login_required(login_url ='login')
def logout(request):
    
    auth.logout(request)
    messages.success(request, 'you are log out')
    return redirect('login')
   # return render(request,'accounts/.html')
   
   
def activate(requsert):
    return  

@login_required(login_url ='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_order=True)
    orders_count=orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile = None
        

    #userprofile=UserProfile.objects.get(user_id=request.user.id)
   
    context={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'accounts/dashboard.html',context)


def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_order=True).order_by('-created_at')
    context={
        'orders':orders
        
    }
    return render(request, 'accounts/my_orders.html',context)

def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method =='POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile is updated')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
         }    
    return render(request ,'accounts/edit_profile.html',context)

   
def display(request):
    product=Products.objects.all().filter(is_available=True)
    context ={
        'product':product,
    }
    return render(request,"welcome.html",context)

#@login_required(login_url ='login')
def order_detail(request):
    return render(request,"accounts/order_detail.html")
    
    