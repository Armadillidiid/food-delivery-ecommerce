from re import A
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
import bcrypt
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

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

        # Validate inputted password
        decryptedPw = check_password(password, user.password)

        # Validate user 
        user = authenticate(request, email=email)
        if decryptedPw is not False:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Passowrd is invalid')

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

        print(form.is_valid)
        print(form.errors)
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


def details(request, id):
    return HttpResponse(f"Testing {id}")
