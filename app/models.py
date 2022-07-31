from django.db import models
import datetime
# Create your models here.


class PostModel(models.Model):

    title = models.CharField(max_length=20)
    heading = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    posted_id = models.IntegerField()
    posted_by = models.CharField(max_length=20)
    posted_on = models.DateField('Date', default=datetime.date.today)
    upi_id = models.CharField(max_length=50)


    pass