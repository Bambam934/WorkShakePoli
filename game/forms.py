from django import forms

class WordForm(forms.Form):
    word = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese la palabra"})
    )
