
from django.db import models
import datetime
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


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


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254,
                     blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
