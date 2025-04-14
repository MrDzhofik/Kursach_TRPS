from django import forms


class IntForm(forms.Form):
    start_point = forms.IntegerField(label="Начальная точка", required=True)
    dynamic_filed_1 = forms.IntegerField(label="Промежуточная точка",
                                         required=True)
    dynamic_filed_2 = forms.IntegerField(label="Промежуточная точка",
                                         required=True)
    end_point = forms.IntegerField(label="Конечная точка", required=True)
