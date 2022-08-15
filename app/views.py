from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import NewPostModel
from django.core.mail import send_mail

# Other Imports
try: 
    from validate_email_address import validate_email
except:
    print("Error: while importing:")

import random

import os

# Create your views here.


def homepage(request):

    posts = NewPostModel.objects.all()
    context = {
        'posts':posts,
    }

    return render(request, 'homepage.html', context)


def log_in(request):

    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'LoggedIn Sucessfully')
            return redirect('/')
        else:
            messages.warning(request, 'Wrong Credentials')
            print('Problem')
            return render(request, 'login_page.html')
    else:        

        return render(request, 'login_page.html')


def log_out(request):
    logout(request)
    messages.success(request, 'You are now logged out !')
    return redirect('/')


def donate_page(request):

    posts = NewPostModel.objects.all()
    context = {
        'posts':posts,
    }

    return render(request, 'donator.html', context)


def sign_up(request):

    if request.method == 'POST':

        # Collect information entered by the user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if password is too short or not
        if len(password1) <8 :
            messages.warning(request, 'Passwrod seems too short, it must at least 8 characters long')
            return redirect('/signup')
        
        # Validate email address
        try:
            isExists = validate_email(email, verify=True)
            if isExists == None:
                messages.warning(request, "The provided email does not exist. Please enter a valid email address")
                return redirect('/signup')
        except:
            print("Continued")

        # Generate username for each user slicing the email address
        generated_userName = email.split('@')
        username = generated_userName[0]

        # Check if password entered are same or not
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already registered')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'This username is already taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1)
                user.save()
                messages.success(
                    request, f'Account created for {first_name} with username - {username} sucessfully')
                try:
                    send_mail(
                        'Welcome Message', 
                        f'Welcome to Fund Raisers\nThank you for registering on our website.\nYour Credentials are as follows :\nUsername : {username}\nPassword : {password1}\n(*Do not share it with anyone)\nLogin and use the most out of this platform!', 
                        'nikofficial25@gmail.com', 
                        [email], 
                        fail_silently=False
                    )
                except Exception as e:
                    print(e)
                    
                return redirect('/')
        else:
            messages.error(request, 'Password not matched')
            return redirect('/signup')

    return render(request, 'signup.html')


@login_required(login_url='/login')
def profile(request):

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        upi_id = request.POST['upi_id']
        by = request.user.username

        # For image upload
        files = request.FILES
        image = files.get("images")

        # Generate unique Id for all posts
        num = random.randint(0,1000000)
        post_id = f"{by}{num}"

        # Create a new object in the database
        try:
            entry = NewPostModel.objects.create(
                title = title,
                description = description,
                upi_id = upi_id,
                posted_by = by,
                post_id = post_id,
            )
            entry.images = image
            entry.save()
            messages.success(request,'Post have been created sucessfully')
            return redirect('/profile')

        except:
            messages.warning(request, 'Unable to process your request')
            return redirect('/profile')

    else:
        return render(request, 'profile.html')