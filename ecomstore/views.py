from django.shortcuts import render,redirect
from . models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from . forms import SignUpForm,UpdateUserForm, ChangePasswordForm
from django.contrib.auth.models import User
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
            messages.success(request,'Registered Successfully...')
            return redirect('home')
        else:
            messages.success(request,'Whoops! There was a problem registering please try again...')
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{'categories':categories})
        