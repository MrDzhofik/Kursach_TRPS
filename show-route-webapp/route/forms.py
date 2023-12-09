from django import forms

class SimpleForm(forms.Form):
    start_point = forms.CharField(label="Start Point", max_length=100)
    end_point = forms.CharField(label="End Point", max_length=100)