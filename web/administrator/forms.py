from django import forms

from main.models import Country


class CountryForm(forms.ModelForm):
    """
    County form.
    """
    class Meta:
        model = Country
        fields = ['name', 'iso2_code']

    name = forms.CharField(
        label='Currency Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'country-name',
                "parsley-trigger": "change",
                'placeholder': 'Enter country name'
            }
        )
    )
    iso2_code = forms.CharField(
        label='ISO Code',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'iso2-code',
                'parsley-trigger': 'change',
                'placeholder': 'Enter ISO code'
            }
        )
    )
    longitude = forms.CharField(
        label='Longitude',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'longitude',
                'parsley-trigger': 'change',
                'placeholder': 'Enter Longitude'
            }
        )
    )
    latitude = forms.CharField(
        label='Latitude',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'latitude',
                'parsley-trigger': 'change',
                'placeholder': 'Enter Latitude'
            }
        )
    )
