from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login
from .forms import MyUserCreationForm
import bcrypt
from .models import User
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.


def loginPage(request):
    if request.method == 'POST':
        # Get user login credentails
        email = request.POST.get("email").lower()
        password = request.POST.get("password").encode('utf-8')
        print(isinstance(password, bytes))
        # Clone user model if it exists
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
            print("User does not exist")

        # Decrypt user password
        hash = user.password
        print(hash, isinstance(hash, str))
        hash = user.password.encode('utf-8')
        print(hash, isinstance(hash, bytes))
        decryptedPw = bcrypt.checkpw(password, hash)
        print(decryptedPw)

        # Validate user
        user = authenticate(request, email=email)
        if decryptedPw is not False:
            login(request, user)
            return redirect('index')

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

        print(form.is_valid)
        print(form.errors)
        messages.error(request, form.errors)
        if form.is_valid():
            # Clone form model
            user = form.save(commit=False)

            

            # Validate password length
            # if len(user.password) > 25:
            #     messages.error(
            #         request, "PASSWORD MUST BE LESS THAN OR EQUAL TO 25 CHARACTER LENGTH")

            # Hash user password
            # bytes = user.password.encode('utf-8')
            # salt = bcrypt.gensalt()
            # hash = bcrypt.hashpw(bytes, salt).decode('utf-8')

            # Save modified form to database
            # user.password = hash
            user.password = make_password(user.password)
            user.save()
            messages.success(request, "ACCOUNT WAS CREATED SUCCESSFULLY")

            return redirect('register')
    # Create empty form
    form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})


def details(request, id):
    return HttpResponse(f"Testing {id}")
