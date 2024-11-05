from django import forms
from .models import screen, show, ticket


class ScreenForm(forms.ModelForm):
    class Meta:
        model = screen
        fields = [
            "screen_name",
            "total_seats",
        ]
        widgets = {
            "screen_name": forms.TextInput(attrs={"class": "form-control"}),
            "total_seats": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ShowForm(forms.ModelForm):
    class Meta:
        model = show
        fields = ["screen", "movie", "show_time", "price", "food_allowed"]
        widgets = {
            "screen": forms.Select(attrs={"class": "form-control"}),
            "movie": forms.Select(attrs={"class": "form-control"}),
            "show_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",  # Enables browser-native datetime picker
                }
            ),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "food_allowed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TicketBookingForm(forms.Form):
    num_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")
