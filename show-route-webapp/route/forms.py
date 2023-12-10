from django import forms
from .models import Attraction

class SimpleForm(forms.Form):
    start_point = forms.ModelChoiceField(queryset=Attraction.objects.all(), label="Start Point", required=True)
    end_point = forms.ModelChoiceField(queryset=Attraction.objects.all(), label="End Point", required=True)