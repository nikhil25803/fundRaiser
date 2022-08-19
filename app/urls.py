from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('donate', views.donate_page, name='donate-page'),
    path('signup', views.sign_up, name='user-register'),
    path('login', views.log_in, name='user-login'),
    path('logout', views.log_out, name='user-logout'),
    path('profile', views.profile, name='profile-page'),
    path('payments/<str:pk>', views.payments, name='payment-page'),
]
