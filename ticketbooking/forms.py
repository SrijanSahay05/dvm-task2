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
        fields = ["screen", "movie", "show_time", "price"]
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
        }


class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = ticket
        fields = ["num_of_seats"]
        widgets = {
            "num_of_seats": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.show_instance = kwargs.pop("show_instance", None)
        super().__init__(*args, **kwargs)
        if self.show_instance:
            # Limit the max number of seats to available seats for the selected show
            self.fields["num_of_seats"].widget.attrs["max"] = (
                self.show_instance.screen.available_seats
            )
