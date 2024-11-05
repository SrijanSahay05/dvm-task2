from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction as db_transaction  # To avoid naming conflict

from .models import Wallet, Transactions
from .forms import DepositForm


@login_required
def deposit_funds(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

            # Ensure only positive deposit amounts
            if amount <= 0:
                messages.error(request, "Deposit amount must be positive.")
                return redirect("deposit-fund")  # Correct URL name for deposit page

            try:
                with db_transaction.atomic():
                    # Lock the wallet row to prevent concurrent modifications
                    wallet = Wallet.objects.select_for_update().get(id=wallet.id)

                    # Deposit funds and record transaction
                    wallet.deposit(amount)
                    Transactions.objects.create(
                        sender_wallet=None,  # No sender for deposit
                        receiver_wallet=wallet,
                        transaction_type="deposit",
                        amount=amount,
                        status="COMPLETE",
                        description="Wallet deposit",
                    )

                messages.success(
                    request, f"Successfully deposited ${amount} to your wallet."
                )
                return redirect(
                    "theatre-dashboard"
                )  # Redirect to the dashboard after deposit
            except Exception as e:
                messages.error(request, f"Error during deposit: {str(e)}")
                return redirect(
                    "deposit-fund"
                )  # Redirect back to deposit page if error occurs
    else:
        form = DepositForm()

    return render(
        request, "transactions/deposit_funds.html", {"form": form, "wallet": wallet}
    )


def make_payment(
    sender_wallet, receiver_wallet, amount, transaction_type, description=""
):
    """
    Handles fund transfer between two wallets and creates a single transaction record.
    """
    if sender_wallet.balance >= amount:
        with db_transaction.atomic():
            # Perform the fund transfer without creating duplicate transactions
            sender_wallet.withdraw(amount)
            receiver_wallet.deposit(amount)

            # Create a single transaction record
            transaction_record = Transactions.objects.create(
                sender_wallet=sender_wallet,
                receiver_wallet=receiver_wallet,
                transaction_type=transaction_type,
                amount=amount,
                status="COMPLETE",
                description=description,
            )
        return transaction_record  # Return transaction for further use if needed
    return None  # Return None if funds are insufficient


@login_required
def revert_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transactions, id=transaction_id, sender_wallet=request.user.wallet
    )
    if transaction.status == "COMPLETE":
        transaction.revert_transaction()
        messages.success(request, "Transaction reverted successfully.")
    else:
        messages.error(request, "Transaction cannot be reverted.")
    return redirect("transaction_history")
