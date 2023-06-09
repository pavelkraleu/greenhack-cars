from django import forms

from web.models import CarDrive


class CarDriveForm(forms.ModelForm):
    class Meta:
        model = CarDrive
        fields = ["proposed_type", "frozen"]
