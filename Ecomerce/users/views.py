from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from myadmin.models import BlockedUser
from myadmin.models import Category,Products,ProductImages
from django.core import signing 
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

def single_product(request,product_id):
    
    product = get_object_or_404(Products, pk=product_id)
    
    return render(request, 'users/singleproduct.html', {'product': product})
def shop(request):
    if request.user.is_authenticated == False:
        return redirect('signup')
    
    products= Products.objects.all()
    images= ProductImages.objects.all()
    return render(request,'users/shop.html',{'products':products,'images':images})

    
