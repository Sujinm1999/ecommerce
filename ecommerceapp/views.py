from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from . models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import User,auth

# Create your views here.

def home(request):
    return HttpResponse("haii guys")

def allProdCat(request,c_slug=None):
    c_page=None
    products=None
    pro=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products=Product.objects.filter(category=c_page,available=True)

    else:
        products=Product.objects.all().filter(available=True)
    paginator=Paginator(products,3)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        pro=paginator.page(page)
    except(EmptyPage,InvalidPage):
        pro=paginator.page(paginator.num_pages)

    return render(request,'category.html',{'category':c_page,'products':pro})

def ProdCatDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password = request.POST['password']
        if username=="admin" and password=="admin":
            return redirect('/admin/')
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['username'] = username
                return redirect('/login/')
            else:
                messages.info(request, 'Invalid details')
                return redirect('/')
    else:
        return render(request,'login.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exist")
                return redirect('/register/r')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Mail ID already exist")
                return redirect('/register/r')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,password=password1)
                user.save()
                return redirect('/')
        else:
            messages.info(request, "Password missmatch")
            return redirect('/register/r')
    else:
        return render(request,'registration.html')

def logout(request):
    auth.logout(request)
    return redirect('/')