
from django.db import models
import datetime
# Create your models here.

class NewPostModel(models.Model):

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/')
    upi_id = models.CharField(max_length=20, default="")
    posted_on = models.DateField(("Date"), default=datetime.date.today)
    posted_by = models.CharField(max_length=20)
    post_id = models.CharField(max_length=10)

    def __str(self):

        return f"{self.title} by {self.posted_on}"