
from django.shortcuts import render,redirect
from cart.models import CartItems,Cart
from .forms import OrderForm
from .models import Order ,OrderProduct
from .models import Payment
import datetime
import json
from store.models import Products
from django.http import JsonResponse



# Razorpay client initialization



def payments(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_order=False,order_number=body['orderID'])
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total, 
        status=body['status'],
        
    )
    payment.save()
    order.payment=payment
    order.is_order=True
    order.save()
    
    
    cart_items=CartItems.objects.filter(user=request.user)
    
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()
        
        
        product =Products.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()
        
        
        
    CartItems.objects.filter(user=request.user).delete()   
    
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
    } 
    return JsonResponse(data)



def place_order(request,total=0,quantity=0,):
    current_user=request.user
    cart_items=CartItems.objects.filter(user=current_user)
    cart_count=cart_items.count()
    
    if cart_count <=0:
        return redirect('store')
    grand_total =0
    tax=0
    
    for cart_item in cart_items:
        total +=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax      
    
    
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data =Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date + str(data.id)
            data.order_number=order_number
            data.save()
            
            order=Order.objects.get(user=current_user,is_order=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')    
            

# Create your views here.

def order_complete(request):
    
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
   
    
    try: 
      order=Order.objects.get(order_number=order_number,is_order=True)
      ordered_product=OrderProduct.objects.filter(order_id=order.id)
      
      subtotal=0
      for i in ordered_product:
          subtotal+=i.product_price*i.quantity
      
      #payment=Payment.objects.get(payment_id=transID)
      context={
        'order':order,
        'ordered_product':ordered_product,
        'order_number':order.order_number,
        'subtotal':subtotal,
        
        #'transID':payment.payment_id,
        #'payment':payment,
        
        }
      return render(request,"orders/order_complete.html",context)
      
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('display') 
    
    
    