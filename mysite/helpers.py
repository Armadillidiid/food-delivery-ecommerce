from .models import *

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