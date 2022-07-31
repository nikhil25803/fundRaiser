
from django.db import models
import datetime

# Create your models here.


class PostModel(models.Model):

    title = models.CharField(max_length=20)
    heading = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    post_id = models.UUIDField(primary_key=True, editable=False)
    posted_by = models.CharField(max_length=20)
    posted_on = models.DateField('Date', default=datetime.date.today)
    upi_id = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):

        return f"{self.title} | Id {self.post_id}"


    pass