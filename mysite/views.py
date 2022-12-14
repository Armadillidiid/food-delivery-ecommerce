from dataclasses import asdict
from itertools import product
from re import A
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from PIL import Image
from .modules.helpers import get_details, sort_location, getOpenHour, createVendorCategoryChoices
from phonenumber_field.phonenumber import PhoneNumber
from random import uniform
import datetime
import json
import uuid
import sys
import os

# Make sure API key is set
if not os.environ.get("MAP_API_KEY"):
    raise RuntimeError('MAP_API_KEY not exist')


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        pass
    form = createVendorCategoryChoices()
    try:
        category = []
        for i in form:
            if (request.GET.get(i[0]) == 'on'):
                category.append(i[0])
    except:
        category = []
        print(sys.exc_info()[1])

    try:
        location = request.GET.get('location')
        print('Default location is: ', location)
        map_location = sort_location(location)
    except:
        map_location = {}
        print("No Map location was detected")

    if category == []:
        if map_location == {}:
                vendors = Vendor.objects.all().order_by('name')
        else:
            vendors = Vendor.objects.filter(state=map_location['state'].lower()).order_by('name')
            print(vendors)
    else:
        if map_location == {}:
                vendors = Vendor.objects.filter(category__in=category).order_by('name')
        else:
            print(category, map_location['state'])
            vendors = Vendor.objects.filter(category__in=category, state=map_location['state'].lower()).order_by('name')
            print("Didn't work did it?")
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
        'map_location': map_location,
        'categories': category,
        'form': form,
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
        db_id =  request.POST.get('db_id')
        form = ShippingAddressForm(request.POST)
        messages.error(request, form.errors)
        if form.is_valid():
            raw_form = form.save(commit=False)

            if (db_id == ''):
                ShippingAddress.objects.create(
                    customer=request.user,
                    contact_name=raw_form.contact_name,
                    address=raw_form.address,
                    state=raw_form.state,
                    city=raw_form.city,
                    zip_code=raw_form.zip_code,
                    number=raw_form.number
                )
            else:
                # Update or create new address
                obj, created = ShippingAddress.objects.update_or_create(
                    id=db_id,
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

            messages.success(request, "Address created successfully")

    form = ShippingAddressForm()
    details = get_details(request, name)
    vendor = Vendor.objects.get(name=name)
    orders = Order.objects.filter(
        customer=details['customer'], is_complete=False)
    items = {}
    for order in orders:
        items[order] = order.orderitem_set.all()
    paymentOrder = Order.objects.get(
        customer=details['customer'], vendor=details['vendor'], is_complete=False)
    shippingAddresses = ShippingAddress.objects.filter(customer=request.user)
    print(shippingAddresses)

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


@login_required(login_url='login')
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


@login_required(login_url='login')
def processOrder(request):
    transaction_id = uuid.uuid4()
    data = json.loads(request.body)

    vendor = data['shippingInfo']['vendor']
    details = get_details(request, vendor)
    total = float(data['paymentInfo']['total'])
    order = Order.objects.get(
        customer=details['customer'], vendor=details['vendor'], is_complete=False)
    shippingAddress = ShippingAddress.objects.get(
        pk=data['shippingInfo']['id'])

    order.transaction_id = transaction_id

    if total == order.get_cart_price + 1:
        shippingAddressOrder = ShippingAddressOrder.objects.create(
            customer=shippingAddress.customer,
            contact_name=shippingAddress.contact_name,
            address=shippingAddress.address,
            city=shippingAddress.city,
            state=shippingAddress.state,
            zip_code=shippingAddress.zip_code,
            number=shippingAddress.number
        )

        order.is_complete = True
        order.shipping_address = shippingAddressOrder

    order.save()

    return JsonResponse("Order completed", safe=False)


@login_required(login_url='login')
def deleteOrder(request):
    data = json.loads(request.body)
    vendor = data['vendor']
    orderId = data['orderId']
    customer = request.user
    vendor = Vendor.objects.get(id=vendor)
    Order.objects.get(id=orderId, customer=customer,
                      vendor=vendor, is_complete=False).delete()

    return JsonResponse("Order deleted", safe=False)


@login_required(login_url='login')
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
                messages.error(request, sys.exc_info()[1])

            return redirect('profile-overview')

    customer = request.user
    form = UserUpdateForm(instance=customer)
    context = {
        'route': 'overview',
        'form': form,
        'customer': customer
    }
    return render(request, 'profile-overview.html', context)


@login_required(login_url='login')
def profileOrder(request):
    customer = request.user
    orders = Order.objects.filter(
        customer=customer, is_complete=True).order_by('-date_order')
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


@login_required(login_url='login')
def profileVoucher(request):
    context = {
        'route': 'vouchers',
    }
    return render(request, 'profile-voucher.html', context)


@login_required(login_url='login')
def profileFavourite(request):
    context = {
        'route': 'favourites'
    }
    return render(request, 'profile-favourite.html', context)


@login_required(login_url='login')
def profileVendor(request):
    if request.method == 'POST':
        vendor = Vendor.objects.get(user=request.user)
        form = registerVendorForm(request.POST, request.FILES, instance=vendor)
        print(form)
        if form.is_valid():
            print('Form is valid')
            try:
                form.save()
                messages.success(request, "Vendor profile updated")
                print('Form updated successfully')
            except:

                messages.error(request, sys.exc_info()[1])
        else:
            messages.error(request, form.errors)

        return redirect('profile-vendor')

    customer = request.user
    try:
        vendor = Vendor.objects.get(user=customer)
    except:
        vendor = None
    try:
        categories = ProductCategory.objects.filter(vendor=vendor)
        products = Product.objects.filter(vendor=vendor)
    except:
        categories = None
        products = None
    try:
        vendor = Vendor.objects.get(user=customer)
    except:
        vendor = None
        
    print(categories, products)
    open_hour = getOpenHour(vendor)
    weekday = [
        ('Sunday', open_hour[0]),
        ('Monday', open_hour[1]),
        ('Tuesday', open_hour[2]),
        ('Wednesday', open_hour[3]),
        ('Thursday', open_hour[4]),
        ('Friday', open_hour[5]),
        ('Saturday', open_hour[6]),
    ]
    form = registerVendorForm(instance=vendor)
    form_two = OpenHourForm()
    form_three = addProduct()
    form_four = addCategory()
    context = {
        'route': 'vendor',
        'vendor': vendor,
        'categories': categories,
        'products': products,
        'form': form,
        'form_two': form_two,
        'form_three': form_three,
        'form_four': form_four,
        'weekday': weekday
    }
    return render(request, 'profile-vendor.html', context)


def registerVendor(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print('User is auth')
            form = registerVendorForm(request.POST, request.FILES)
            if form.is_valid():
                print('Form is valid')
                unsaved_form = form.save(commit=False)  
                unsaved_form.banner_image = unsaved_form.image

                # Randomize ratings 
                unsaved_form.ratings= round(uniform(0, 5), 2)
                unsaved_form.user = request.user

                try:
                    unsaved_form.save()
                    messages.success(
                        request, 'Vendor profile created successfully')
                except:
                    messages.error(request, sys.exc_info()[1])

                return redirect('register-vendor')
            else:
                messages.error(request, form.errors)
        else:
            return redirect('login')
    form = registerVendorForm()
    context = {
        'form': form
    }
    return render(request, 'register-vendor.html', context)


def deleteVendor(request):
    Vendor.objects.get(user=request.user).delete()
    return redirect('profile-vendor')


def queryGoogleMap(request):
    data = json.loads(request.body)
    string = data['string']
    key = os.environ["MAP_API_KEY"]
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={string}&key={key}&libraries=places&types=geocode&components=country:ng"

    response = requests.request("GET", url)
    new_data = response.json()

    return JsonResponse(new_data, safe=True)


def createUpdateOpenHours(request):
    data = json.loads(request.body)
    try:
        model_id = data['model_id']
    except:
        model_id = None
    print(model_id)
    open_time = data['open_time']
    close_time = data['close_time']
    weekday = data['weekday'][0:3]
    vendor_name = data['vendor']
    vendor = Vendor.objects.get(name=vendor_name)

    if model_id == '':
        OpenHour.objects.create(
            open_time=open_time,
            close_time=close_time,
            weekday=weekday,
            vendor=vendor
            )
    else:
        OpenHour.objects.update_or_create(
            id=model_id,
            defaults= {
                'open_time': open_time,
                'close_time': close_time,
                'weekday': weekday,
                'vendor': vendor,
            }
        )
    open_hour = OpenHour.objects.get(vendor=vendor, weekday=weekday)
    return_data = {}
    return_data['model_id'] = open_hour.id
    return_data['weekday'] = data['weekday']
    return JsonResponse(return_data, safe=True)


def deleteOpenHour(request):
    data = json.loads(request.body)
    model_id = data['model_id']
    OpenHour.objects.get(id=model_id).delete()
    return JsonResponse("Deleted Successfully", safe=False)


def deleteUser(request):
    customer = request.user
    User.objects.get(id=customer.id).delete()
    return redirect('index')


def createProduct(request):
    if request.method == 'POST':
        form = addProduct(request.POST, request.FILES)
        category = request.POST.get('category')
        if form.is_valid():
            vendor = Vendor.objects.get(user=request.user)
            unsaved_form = form.save(commit=False)
            unsaved_form.category = ProductCategory.objects.get(name=category, vendor=vendor)
            unsaved_form.vendor = vendor
            unsaved_form.save()
            try:    
                messages.success(request, 'Product Created')
            except:
                messages.error(request, form.errors)

    return redirect('profile-vendor')


def createCategory(request):
    if request.method == 'POST':
        form = addCategory(request.POST)
        if form.is_valid():
            vendor = Vendor.objects.get(user=request.user)
            unsaved_form = form.save(commit=False)
            unsaved_form.vendor = vendor
            try:
                form.save()
                messages.success(request, 'Category created')
            except:
                messages.error(request, form.errors)

    return redirect('profile-vendor')