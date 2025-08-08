from django.shortcuts import render,redirect
from . models import Product,Category, Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from . forms import SignUpForm,UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.db.models import Q
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
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
           
            messages.success(request,'User Info Updated!!!')
            return redirect('home')
        return render(request,'update_info.html',{'form':form})
    else:
        messages.error(request,'You must logged in to access this page!!!')
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) or Q(description__icontains=searched))
        if not searched:
            messages.error(request,'That Product Doesnt exist please try again...')
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})