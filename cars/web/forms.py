from django import forms

from web.models import CarDrive, Analysis


class CarDriveForm(forms.ModelForm):
    class Meta:
        model = CarDrive
        fields = ["proposed_type", "frozen"]
        help_texts = {
            "proposed_type": "You can hardcode some car for this license plate. For example CEO of the company "
            "may have car which is higher class than "
            "it should have according to his/her driving needs.",
            "frozen": "This car will be ignored in analysis and proposed type will not be changed.",
        }


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ["replace_min_age_years", "replace_min_odometer_km"]
        labels = {
            "replace_min_age_years": "Minimum car age to be replaced",
            "replace_min_odometer_km": "Minimum kilometers driven to be replaced",
        }
        help_texts = {
            "replace_min_age_years": "Car must be older than this value in order to be replaced. "
            "For example you do not want to replace one year old car.",
            "replace_min_odometer_km": "Car must have driven at least this number of kilometers to be replaced. "
            "For example you do not want to replace cars which have drive only 10 000 km",
        }
