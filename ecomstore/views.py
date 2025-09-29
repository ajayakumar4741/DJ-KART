from django.shortcuts import render,redirect
from . models import Product,Category, Profile, PasswordResetRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from . forms import SignUpForm,UpdateUserForm, ChangePasswordForm, UserInfoForm
from payments.forms import ShippingForm
from payments.models import ShippingAddress
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart
from django.utils.crypto import get_random_string
# Create your views here.

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your Password is updated, please log in again !!!')
                # login(request,current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
        else:
            form = ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,'You must logged in to access this page!!!')
        return redirect('home')
    
def reset_password(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()
    
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('home')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'reset-password.html', {'token': token})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        
        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found.')
    
    return render(request, 'forgot-password.html')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,'User Profile Updated!!!')
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.error(request,'You must logged in to access this page!!!')
        return redirect('home')
    

def category(request,foo):
    foo = foo.replace('-',' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products, 'category':category})
    except Category.DoesNotExist:
        messages.error(request,'That category doesnt exist...')
        return redirect('home')
    
def home(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
                    
            messages.success(request,'You have logged in successfully...')
            return redirect('home')
        else:
            messages.success(request,'There was an error, please try again later')
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,'Logout Successfully...')
    return redirect(reverse('login'))
        
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,'User Created please fill this form...')
            return redirect('update_info')
        else:
            messages.success(request,'Whoops! There was a problem registering please try again...')
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{'categories':categories})
        
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = None
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save() 
            messages.success(request,'User Info Updated!!!')
            return redirect('home')
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.error(request,'You must logged in to access this page!!!')
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.error(request,'That Product Doesnt exist please try again...')
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})