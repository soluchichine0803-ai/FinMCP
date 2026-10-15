from django.conf import settings
from django.db import models


class Account(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="accounts"
    )
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="NGN")
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return self.account_number