
from turtle import title
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
# from requests import head
# Create your views here.


def homepage(request):

    return render(request, 'homepage.html')


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
    return redirect('/')


def donate_page(request):

    return render(request, 'donator.html')


def sign_up(request):

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # username = request.POST.get('uname', 'user')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        generated_userName = email.split('@')
        username = generated_userName[0]

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
                        'Subject here', 
                        'Here is the message.', 
                        'nikhil25803@gmail.com', 
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
        # img = request.POST['images']

        print(title, ' BY ', upi_id)
        return redirect('/profile')


    return render(request, 'profile.html')