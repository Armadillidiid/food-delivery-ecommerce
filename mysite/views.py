from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import MyUserCreationForm
import bcrypt

# Create your views here.
def loginPage(request):
    return render(request, 'login.html')

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
        if form.is_valid():
            # Clone form model
            user = form.save(commit=False)
            password = user.password

            # Validate password length
            if len(password) > 25:
                messages.error(
                    request, "PASSWORD MUST BE LESS THAN OR EQUAL TO 25 CHARACTER LENGTH")

            # Hash user password
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)

            # Save modified form to database
            user.password = hash
            user.save()
            messages.success(request, "ACCOUNT WAS CREATED SUCCESSFULLY")
            
            return render('register')
    # Create empty form
    form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})


def details(request, id):
    return HttpResponse(f"Testing {id}")
