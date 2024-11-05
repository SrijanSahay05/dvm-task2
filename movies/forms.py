from django import forms
from .models import Movie


class MovieAddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "genre",
            "description",
            "release_date",
            "rating",
            "duration",
            "director",
        ]
        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}),
        }
