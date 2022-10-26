from re import A
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, ShippingAddressForm
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from PIL import Image
import datetime, json


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        pass
    vendors = Vendor.objects.all().order_by('name')
    # size = (360, 200)
    # for vendor in vendors:
    #     try:
    #         image = Image.open(vendor.image)
    #     except:
    #         continue
    #     image.thumbnail(size)
    #     image.save(vendor.image.path)

    customer = request.user
    orders = Order.objects.filter(customer=customer, is_complete=False)
    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

    context = {
        'vendors': vendors,
        'orders': orders,
        'items': items,
        }
    return render(request, 'home.html', context)


def loginPage(request):
    if request.method == 'POST':
        # Get user login credentails
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        # Clone user model if it exists
        try:
            user = User.objects.get(email=email)
        except:
            print('User does not exist')
            messages.error(request, "User does not exist")
            return render(request, 'login.html')


        # Validate inputted password
        decryptedPw = check_password(password, user.password)

        # Validate user 
        user = authenticate(request, email=email, password=password)
        if decryptedPw is not False:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Passoword is invalid')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')


def index(request):
    """First view function."""
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def faqs(request):
    return render(request, 'faqs.html')


def register(request):
    if request.method == "POST":
        # Populate form using submitted data
        form = MyUserCreationForm(request.POST)
        messages.error(request, form.errors)
        if form.is_valid():
            # Clone form model
            user = form.save(commit=False)

            # Hash user password
            user.password = make_password(user.password)

            # Add user to database
            user.save()
            messages.success(request, "ACCOUNT WAS CREATED SUCCESSFULLY")
            
    # Create empty form
    form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def store(request,  name):
    customer = request.user
    vendor = Vendor.objects.get(name=name)
    products = Product.objects.filter(vendor=vendor.id)
    categories = ProductCategory.objects.filter(vendor=vendor.id)
    open_hours = OpenHour.objects.filter(vendor=vendor.id)
    orders = Order.objects.filter(customer=customer, is_complete=False)

    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

    # Get current date and time
    e = datetime.datetime.now()
    current_day =  e.strftime("%a")
    current_time = e.strftime("%H:%M:%S")

    # Check if store is open
    is_open = False
    for open_hour in open_hours:
        if current_day == open_hour.weekday:
            is_open = True
            break

    
    context = {
        'vendor': vendor,
        'products': products,
        'categories': categories,
        'open_hours': open_hours,
        'current_day': current_day,
        'current_time': current_time,
        'is_open': is_open,
        'orders': orders,
        'items': items,
        'iterator': range(1,26)
        }

    return render(request, 'store.html', context)


@login_required(login_url='login')
def checkout(request, name):
    if request.method == 'POST':
        pass
    
    form = ShippingAddressForm()
    details = get_details(request, name)
    orders = Order.objects.filter(customer=details['customer'], is_complete=False)
    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

   

    context = {
        'details': details,
        'orders': orders,
        'items': items,
        'form': form
    }
    return render(request, 'checkout.html', context)


def get_details(request, name):
    customer = request.user
    vendor = Vendor.objects.get(name=name)
    products = Product.objects.filter(vendor=vendor.id)
    categories = ProductCategory.objects.filter(vendor=vendor.id)
    open_hours = OpenHour.objects.filter(vendor=vendor.id)
    orders = Order.objects.filter(customer=customer, is_complete=False)

    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

    context = {
        'customer': customer,
        'vendor': vendor,
        'products': products,
        'categories': categories,
        'open_hours': open_hours,
        'orders': orders,
        'items': items,
        }
    
    return context

def updateCart(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse("Item added to cart", safe=False)



