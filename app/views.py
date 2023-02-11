
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import NewPostModel
from django.core.mail import send_mail
import razorpay
from .constants import PaymentStatus
from .models import Order
from raiser import settings
import json
from django.views.decorators.csrf import csrf_exempt
# Other Imports
try:
    from validate_email_address import validate_email
except:
    print("Error: while importing:")
import random
import pyqrcode


# Homepage
def homepage(request):

    # Fetching data from the Model
    posts = NewPostModel.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'homepage.html', context)


# Login Page
def log_in(request):

    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'LoggedIn Sucessfully')
            return redirect('/')
        else:
            messages.warning(request, 'Wrong Credentials')
            return render(request, 'login_page.html')
    else:

        return render(request, 'login_page.html')


# Logout Call
def log_out(request):

    logout(request)

    messages.success(request, 'You are now logged out !')
    return redirect('/')


# Page containing all the posts
def donate_page(request):

    posts = NewPostModel.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'donator.html', context)

# Sign-up Page


def sign_up(request):

    if request.method == 'POST':

        # Collect information entered by the user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if password is too short or not
        if len(password1) < 8:
            messages.warning(
                request, 'Passwrod seems too short, it must at least 8 characters long')
            return redirect('/signup')

        # Validate email address
        try:
            isExists = validate_email(email, verify=True)
            if isExists == None:
                messages.warning(
                    request, "The provided email does not exist. Please enter a valid email address")
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

    # Get filtered data from the Models
    by_user = request.user.username
    user_posts = NewPostModel.objects.filter(posted_by=f'{by_user}')
    context = {
        'user_posts': user_posts,
    }

    # Create post feature for the users
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        upi_id = request.POST['upi_id']
        by = request.user.username

        # For image upload
        files = request.FILES
        image = files.get("images")

        # Generate unique Id for all posts
        num = random.randint(0, 1000000)
        post_id = f"{by}{num}"

        # Create a new object in the database
        try:
            entry = NewPostModel.objects.create(
                title=title,
                description=description,
                upi_id=upi_id,
                posted_by=by,
                post_id=post_id,
            )
            entry.images = image
            entry.save()
            messages.success(request, 'Post have been created sucessfully')
            return redirect('/profile')

        except:
            messages.warning(request, 'Unable to process your request')
            return redirect('/profile')

    else:
        return render(request, 'profile.html', context)


@login_required(login_url='/login')
def payments(request, pk):

    # Filtering out posts on the basis of Post Id
    posts = NewPostModel.objects.filter(post_id=f"{pk}")
    details = []
    for post in posts:
        details.append(post.post_id)
        details.append(post.upi_id)
    by = request.user.username
    upi_id = details[1]

    # Generating QR Code for Payments in SVG form and storing in the media folder
    upiUrl = f'upi://pay?pn={by}&pa={upi_id}&cu=INR'
    url = pyqrcode.create(upiUrl)
    ans = url.svg('./media/'+f"{details[0]}.svg", scale=8)

    return render(request, 'payments.html', {'posts': posts})


@login_required(login_url='/login')
def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mail = request.POST.get("email")
        mobile = request.POST.get("mobilenumber")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR",
             "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
                "name":name,
                "email":mail,
                "mobile":mobile,
                "description":description
            },
        )
    return render(request, "payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get(
            "error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})
