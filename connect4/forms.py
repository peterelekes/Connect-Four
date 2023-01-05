from django import forms

class MoveForm(forms.Form):
    column = forms.IntegerField(min_value=0, max_value=6)

