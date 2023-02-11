from django.contrib import admin
from .models import NewPostModel, Order


admin.site.register(NewPostModel)
admin.site.register(Order)