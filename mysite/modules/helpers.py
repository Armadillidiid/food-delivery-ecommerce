import mysite.models

nigerian_capital = [
    ('Umuahia', 'Abia'),
    ('Abuja', 'Abuja'),
    ('Yola', 'Adamawa'),
    ('Uyo', 'Akwa_ibom'),
    ('Awka', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Yenagoa', 'Bayelsa'),
    ('Makurdi', 'Benue'),
    ('Maiduguri', 'Borno'),
    ('Calabar', 'Cross River'),
    ('Asaba', 'Delta'),
    ('Abakaliki', 'Ebonyi'),
    ('Benin City', 'Edo'),
    ('Ado Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Owerri', 'Imo'),
    ('Dutse', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Birnin Kebbi', 'Kebbi'),
    ('Lokoja', 'Kogi'),
    ('Ilorin', 'Kwara'),
    ('Ikeja', 'Lagos'),
    ('Lafia', 'Nasarawa'),
    ('Minna', 'Niger'),
    ('Abeokuta', 'Ogun'),
    ('Akure', 'Ondo'),
    ('Oshogbo', 'Osun'),
    ('Ibadan', 'Oyo'),
    ('Jos', 'Plateau'),
    ('Port Harcourt', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Jalingo', 'Taraba'),
    ('Damaturu', 'Yobe'),
    ('Gusau', 'Zamfara')
]


def get_details(request, name):
    customer = request.user
    print(name)
    vendor = mysite.models.Vendor.objects.get(name=name)
    products = mysite.models.Product.objects.filter(vendor=vendor.id)
    categories = mysite.models.ProductCategory.objects.filter(vendor=vendor.id)
    open_hours = mysite.models.OpenHour.objects.filter(vendor=vendor.id)
    orders = mysite.models.Order.objects.filter(
        customer=customer, is_complete=False)

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


def sort_location(location):
    location_list = location.split(',')
    location = {
        'address': location_list[0].strip(),
        'state': location_list[1].strip(),
        'country': location_list[2].strip()
    }
    for capital in nigerian_capital:
        for i in capital:
            if location['state'] == i:
                location['state'] = capital[1]
                break
    return location


def createCategory():
    category = [
        ('african', 'African'),
        ('alcoholic drinks', 'Alcoholic Drinks'),
        ('bakery and cakes', 'Bakery and Cakes'),
        ('breakfast', 'Breakfast'),
        ('chinese', 'Chinese'),
        ('fast food', 'Fast Food'),
        ('grills', 'Grills'),
        ('ice cream', 'Ice Cream'),
        ('pizza', 'Pizza'),
        ('vegan', 'Vegan'),
    ]
    return category


def getOpenHour(vendor):
    open_hour = []
    weekday = [
        'Sun',
        'Mon',
        'Tue',
        'Wed',
        'Thu',
        'Fri',
        'Sat',
    ]
    for day in weekday:
        try:
            print(day)
            open_hour.append(mysite.models.OpenHour.objects.get(
                vendor=vendor, weekday=day))
        except:
            open_hour.append('')

    return open_hour
