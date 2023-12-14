from django.shortcuts import render, redirect
from accounts import form
from django.urls import reverse ,reverse_lazy
from django.contrib.auth import login as auth_login,authenticate,logout as auth_logout
from accounts.form import CustomUserCreationForm
from accounts.models import CustomUser
from myadmin.models import BlockedUser 
from django.core import signing 
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import pyotp




def send_otp_email(user):
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key, digits=6, interval=60)
    otp = totp.now()
    user.otp_secret_key = secret_key
    user.otp = otp
    user.save()

    subject = 'OTP Verification'
    message = f'Your OTP for email verification is: {otp}'
    from_email = 'mjunni99@gmail.com'
    to_email = user.email

    send_mail(subject, message, from_email, [to_email])
@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def signup(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until OTP verification
            user.save()

            # Invalidate any existing OTP for the user
            user.otp = None
            user.save()

            send_otp_email(user)

            messages.success(request, 'Account created successfully. Please check your email for OTP verification.')
            return redirect('verify_otp', user_id=user.id)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/usignup.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def login(request):
    user = None  # Initialize user variable

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")

        if user is not None:
            # Check if the user is blocked
            blocked_user = BlockedUser.objects.filter(user=user).first()
            
            if blocked_user:
                messages.warning(request, "User is blocked by admin.")
            else:
                authenticated_user = authenticate(request, email=email, password=password)
                
                if authenticated_user is not None:
                    auth_login(request, authenticated_user)
                    return redirect("home")
                else:
                    messages.warning(request, "Invalid password")
        else:
            messages.warning(request, "User doesn't exist, Create an account")

    return render(request, 'accounts/ulogin.html', {'user': user})



@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('signup')


@cache_control(no_cache=True, must_revalidate=True, no_store=False)
def verify_otp(request, user_id):
    if request.user.is_authenticated and request.user.is_active :
        return redirect('home')
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        entered_otp = ''.join(request.POST.getlist('otp'))
        totp = pyotp.TOTP(user.otp_secret_key, digits=6, interval=60)
        print("Entered OTP:", entered_otp)
        print("Expected OTP:", totp.now())
        if totp.verify(entered_otp):
            user.is_active = True
            user.save()
            auth_login(request, user)
            messages.success(request, 'OTP verified successfully. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect OTP. Please try again.')

    return render(request, 'accounts/otp.html', {'user': user})


def resend_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    
    # Invalidate any existing OTP for the user
    user.otp = None
    user.save()

    send_otp_email(user)

    messages.success(request, 'OTP resent successfully. Please check your email for the new OTP.')
    return redirect('verify_otp', user_id=user.id)


def home(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated == False:
        return redirect('signup')
    
    
    return render(request,'accounts/ushome.html')

    