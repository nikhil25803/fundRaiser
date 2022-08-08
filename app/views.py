import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import NewPostModel

# Other Imports
try: 
    from validate_email_address import validate_email
except:
    print("Error: while importing:")


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
    return redirect('/')


def donate_page(request):

    posts = NewPostModel.objects.all()
    context = {
        'posts':posts,
    }

    return render(request, 'donator.html', context)


def sign_up(request):

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # username = request.POST.get('uname', 'user')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(password1) <8 :
            messages.warning(request, 'Passwrod seems too short, it must at least 8 characters long')
            return redirect('/signup')
        
        try:
            isExists = validate_email(email, verify=True)
            if isExists == None:
                messages.warning(request, "The provided email does not exist. Please enter a valid email address")
                return redirect('/signup')
        except:
            print("Error")


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
        by = request.user.username
        files = request.FILES
        image = files.get("images")
        print(image)

        try:
            entry = NewPostModel.objects.create(
                title = title,
                description = description,
                upi_id = upi_id,
                posted_by = by,
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