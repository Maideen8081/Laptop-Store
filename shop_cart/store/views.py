from django.shortcuts import render,get_object_or_404,redirect
from .models import Products
from .models import Category
from cart.models import CartItems 
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct





# Create your views here.

def store(request,category_slug=None):
    
    categories=None
    product=None
    
    
    if category_slug != None:
        categories=get_object_or_404(Category,slug=category_slug)
        product=Products.objects.filter(category=categories,is_available=True)
        paginator=Paginator(product,20)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=product.count()
        
        
    else:    
        product=Products.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(product,24)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=product.count()
    context ={
        'product':paged_product,
        'product_count':product_count,
        
        
    }
    
    return render(request,"store/store.html", context)

def product_details(request,category_slug,products_slug):
    
    try:
        product=Products.objects.all().filter(is_available=True)
        single_product=Products.objects.get(category__slug=category_slug,slug=products_slug)
        in_cart=CartItems.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
       
        
    except Exception as e:
        raise e  
    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
        
    else:
         orderproduct=None
    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)        
            
    
    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'product':product,
        'orderproduct':orderproduct,
        'reviews':reviews
    }  
   
    
    return render(request,"store/product_details.html",context)
    



#Search Function


def search(request):
    
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Products.objects.order_by('-create_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=product.count()
    context={
        'product':product,
        'product_count': product_count,
    }        
    return render(request,'store/store.html',context)


def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method =='POST':
        try:
            reviews= ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank You Your review has been updated ')
            return redirect(url)
            
            
        except ReviewRating.DoesNotExist:
            form =ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
               
                data.ip=request.META.get('REMOT_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank You Your review has been submitted ')
                return redirect(url)
            
            
            
            
            
            
            
                
    
