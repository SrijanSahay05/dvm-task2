from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: ${self.balance}"

    def deposit(self, amount):
        # Update balance without creating a transaction record
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            # Update balance without creating a transaction record
            self.balance -= amount
            self.save()
            return True
        return False


class Transactions(models.Model):
    STATUS_CHOICES = [
        ("INCOMPLETE", "Incomplete"),
        ("COMPLETE", "Complete"),
        ("REVERTED", "Reverted"),
    ]
    TYPE_CHOICES = [
        ("ticket_booking", "Ticket Booking"),
        ("food_ordering", "Food Ordering"),
        ("fund_transfer", "Fund Transfer"),
    ]

    sender_wallet = models.ForeignKey(
        Wallet,
        related_name="sent_transactions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    receiver_wallet = models.ForeignKey(
        Wallet,
        related_name="received_transactions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="INCOMPLETE"
    )
    description = models.CharField(max_length=255, blank=True)

    def complete_transaction(self):
        if (
            self.status == "INCOMPLETE"
            and self.sender_wallet
            and self.sender_wallet.withdraw(self.amount)
        ):
            self.receiver_wallet.deposit(self.amount)
            self.status = "COMPLETE"
            self.save()

    def revert_transaction(self):
        if (
            self.status == "COMPLETE"
            and self.receiver_wallet
            and self.receiver_wallet.withdraw(self.amount)
        ):
            self.sender_wallet.deposit(self.amount)
            self.status = "REVERTED"
            self.save()
