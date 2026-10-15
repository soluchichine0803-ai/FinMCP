import uuid
from django.db import models
from Accounts.models import Account


class Transaction(models.Model):
    tid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    from_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="outgoing_transactions"
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="incoming_transactions"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tid)