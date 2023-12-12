from django import forms
from .models import Attraction

class SimpleForm(forms.Form):
    start_point = forms.ModelChoiceField(queryset=Attraction.objects.all(), label="Начальная точка", required=True, )
    # start_filter = forms.ModelChoiceField(queryset=Attraction.objects.values('id'), label='Фильтр', required=False)
    end_point = forms.ModelChoiceField(queryset=Attraction.objects.all(), label="Конечная точка", required=True)
    # end_filter = forms.ModelChoiceField(queryset=Attraction.objects.values('id'), label='Фильтр', required=False)