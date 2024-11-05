from django import forms


class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Amount to Deposit",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
