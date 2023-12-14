from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import CustomUser

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
    