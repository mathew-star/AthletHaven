from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import CustomUser
from myadmin.models import BlockedUser,Products,ProductImages
from django.shortcuts import render, get_object_or_404, redirect
from myadmin.forms import CategoryForm
from django.apps import apps
Category = apps.get_model('myadmin', 'Category')

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def adminlogin(request):
    user = None

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminhome')
    
    if request.method == 'POST':
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:  # Use the specific exception
            messages.warning(request, f"Admin with {email} does not exist")

        if user is not None:
            auth_user = authenticate(request, username=email, password=password)

            if auth_user:
                if auth_user.is_superuser:
                    login(request, user)
                    return redirect('adminhome')
                else:
                    messages.warning(request, 'You do not have permission to access this page!')
            else:
                messages.warning(request, "Invalid password")
    print("not post")
    return render(request, 'myadmin/adminlogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def adminlogout(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    messages.success(request, 'You have been successfully logged out.')
    logout(request)
    return redirect('adminlogin')


def adminhome(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'myadmin/adminhome.html')
    return redirect('adminlogin')
    

def user_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id=user_id)  # Use your custom user model

        if action == 'Block':
            
            if not BlockedUser.objects.filter(user=user).exists():
                BlockedUser.objects.create(user=user)
                user.is_active = False  

        elif action == 'Unblock':
            
            blocked_user = BlockedUser.objects.filter(user=user).first()
            if blocked_user:
                blocked_user.delete()
                user.is_active = True  

        elif action == 'Edit':
            
            return redirect('edit_user', user_id=user_id)

        user.save() 
        return redirect('user_management_view')  

    users = CustomUser.objects.all()  # Use your custom user model
    return render(request, 'myadmin/user_management.html', {'users': users})


def edit_user_view(request, user_id):
 user = CustomUser.objects.get(id=user_id)
 if request.method == 'POST':
     user.name = request.POST.get('name')
     user.email = request.POST.get('email')
     user.phone_number = request.POST.get('phone_number')
     user.save()
     return redirect('user_management_view')
 return render(request, 'myadmin/edituser.html', {'user': user})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'myadmin/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'myadmin/add_category.html', {'form': form})

def toggle_category_listing(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_listed = not category.is_listed
    category.save()
    return redirect('category_list')


def toggle_product_listing(request, category_id):
    p = Products.objects.get(id=category_id)
    p.is_listed = not p.is_listed
    p.save()
    return redirect('product_list')


def product_list(request):
    products = Products.objects.all()
    return render(request, 'myadmin/product_list.html', {'products': products})

def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        rating = request.POST.get('rating')
        star = request.POST.get('star')

        if name and description and category_id and price and rating and star:
            category = Category.objects.get(id=category_id)

            product = Products.objects.create(
                name=name,
                description=description,
                category=category,
                price=price,
                rating=rating,
                star=star
            )

            for i in range(1, 5):
                image = request.FILES.get(f'image{i}')
                if image:
                    ProductImages.objects.create(product=product, image=image)

            return redirect('product_list')

    return render(request, 'myadmin/add_product.html', {'categories': categories})

def edit_product(request, product_id):
  categories = Category.objects.all()
  product = Products.objects.get(id=product_id)
  if request.method == 'POST':
      product.name = request.POST['name']
      product.description = request.POST['description']
      product.price = request.POST['price']
      product.rating = request.POST['rating']
      product.star = request.POST['star']
      product.category = Category.objects.get(id=request.POST['category'])
      product.save()

      for i in range(2): # Update 4 images
          product_image = ProductImages.objects.get(product=product, image=request.FILES[f'image{i+1}'])
          product_image.image = request.FILES[f'image{i+1}']
          product_image.save()

      return redirect('product_list')
  return render(request, 'myadmin/edit_product.html', {'categories': categories})
