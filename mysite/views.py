from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    """First view function."""
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faqs(request):
    return render(request, 'faqs.html')

def details(request, id): 
    return HttpResponse(f"Testing {id}")
