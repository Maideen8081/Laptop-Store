from django .shortcuts import render
from store.models import Products



def display(request):
    product=Products.objects.all().filter(is_available=True)
    context ={
        'product':product,
    }
    return render(request,"welcome.html",context)