from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    """First view function."""
    return render(request, 'indextwo.html')

def details(request, id): 
    return HttpResponse(f"Testing {id}")
