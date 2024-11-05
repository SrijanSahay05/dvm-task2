from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from transactions.models import Wallet


class Command(BaseCommand):
    help = "Create a system wallet for transactions."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        system_user, created = User.objects.get_or_create(
            username="system", defaults={"is_active": False}
        )
        wallet, _ = Wallet.objects.get_or_create(user=system_user)
        self.stdout.write(self.style.SUCCESS("System wallet created or retrieved."))
