from dataclasses import asdict
from itertools import product
from re import A
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, ShippingAddressForm, UserUpdateForm
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from PIL import Image
import datetime
import json
import uuid
import sys
from .helpers import get_details

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
        'iterator': range(1, 26)

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
    details = get_details(request, name)

    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

    # Get current date and time
    e = datetime.datetime.now()
    current_day = e.strftime("%a")
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
        'details': details,
        'iterator': range(1, 26)
    }

    return render(request, 'store.html', context)


@login_required(login_url='login')
def checkout(request, name):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        messages.error(request, form.errors)
        if form.is_valid():
            raw_form = form.save(commit=False)
            
            # Update or create new address 
            obj, created = ShippingAddress.objects.update_or_create(
                id=raw_form.db_id,
                defaults={
                    'customer': request.user,
                    'contact_name': raw_form.contact_name,
                    'address': raw_form.address,
                    'state': raw_form.state,
                    'city': raw_form.city,
                    'zip_code': raw_form.zip_code,
                    'number': raw_form.number
                }
            )
            obj.save()
 

            messages.success(request, "Address created successfully")

    form = ShippingAddressForm()
    details = get_details(request, name)
    vendor = Vendor.objects.get(name=name)
    orders = Order.objects.filter(
        customer=details['customer'], is_complete=False)
    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()
    paymentOrder = Order.objects.get(customer=details['customer'], vendor=details['vendor'], is_complete=False)
    shippingAddresses = ShippingAddress.objects.filter(customer=request.user)

    context = {
        'details': details,
        'vendor': vendor,
        'orders': orders,
        'paymentOrder': paymentOrder,
        'items': items,
        'form': form,
        'shippingAddresses': shippingAddresses,
        'iterator': range(1, 26)
    }
    return render(request, 'checkout.html', context)


def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    vendor_id = data['vendor']
    vendor = Vendor.objects.get(pk=vendor_id)
    try:
        quantity = int(data['quantity'])
    except:
        print("No quantity was submitted")
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, vendor=vendor, is_complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        product=product, order=order)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    elif action == "select":
        orderItem.quantity = quantity
        print(orderItem.quantity)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item added to cart", safe=False)

def processOrder(request):
    transaction_id = uuid.uuid4()
    data = json.loads(request.body)

    vendor = data['shippingInfo']['vendor']
    details = get_details(request, vendor)
    total = float(data['paymentInfo']['total'])
    order = Order.objects.get(customer=details['customer'], vendor=details['vendor'], is_complete=False)
    shippingAddress = ShippingAddress.objects.get(pk=data['shippingInfo']['id'])

    order.transaction_id = transaction_id

    if total == order.get_cart_price + 1:
        shippingAddressOrder = ShippingAddressOrder.objects.create(
        customer=shippingAddress.customer,
        contact_name= shippingAddress.contact_name,
        address = shippingAddress.address,
        city = shippingAddress.city,
        state = shippingAddress.state,
        zip_code= shippingAddress.zip_code,
        number= shippingAddress.number
        )

        order.is_complete = True
        order.shipping_address = shippingAddressOrder


    order.save()

    return JsonResponse("Order completed", safe=False)


def deleteOrder(request):
    data = json.loads(request.body)
    vendor = data['vendor']
    orderId = data['orderId']
    customer = request.user
    vendor = Vendor.objects.get(id=vendor)
    Order.objects.get(id=orderId, customer=customer, vendor=vendor, is_complete=False).delete()

    return JsonResponse("Order deleted", safe=False)



def profileOverview(request):
    if request.method == "POST":
        customer = request.user
        form = UserUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            unclean_form = form.save(commit=False)

            # Encrypt password 
            unclean_form.password = make_password(unclean_form.password)

            # Update existing instance of 'User'
            try:
                unclean_form.save()
                messages.success(request, "Update Successful")
            except:
                messages.error(request, form.errors)

            return redirect('profile-overview')

    customer = request.user
    form = UserUpdateForm(instance=customer)
    context = {
        'route': 'overview',
        'form': form,
        'customer': customer
    }
    return render(request, 'profile-overview.html', context)


def profileOrder(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer, is_complete=True).order_by('-date_order')
    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()

    context = {
        'route': 'orders',
        'customer': customer,
        'orders': orders,
        'items': items
    }
    return render(request, "profile-order.html", context)


def profileVoucher(request):
    context = {
        'route': 'vouchers',
    }
    return render(request, 'profile-voucher.html', context)


def profileFavourite(request):
    context = {
        'route': 'favourites'
    }
    return render(request, 'profile-favourite', context)