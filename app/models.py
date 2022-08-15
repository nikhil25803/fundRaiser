
from django.db import models
import datetime
# Create your models here.


class NewPostModel(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    images = models.ImageField(upload_to='images/')
    upi_id = models.CharField(max_length=30, default="")
    posted_on = models.DateField(("Date"), default=datetime.date.today)
    posted_by = models.CharField(max_length=50)
    post_id = models.CharField(max_length=50)

    def __str__(self):

        return f"{self.title} by {self.posted_by}"
