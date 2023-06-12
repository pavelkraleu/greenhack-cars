from django import forms

from web.models import CarDrive


class CarDriveForm(forms.ModelForm):
    class Meta:
        model = CarDrive
        fields = ["proposed_type", "frozen"]
        help_texts = {
            "proposed_type": "You can hardcode some car for this license plate.",
            "frozen": "This car will be ignored in analysis and proposed type will not be changed.",
        }
