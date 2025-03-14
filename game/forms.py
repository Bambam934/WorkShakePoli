from django import forms

class WordForm(forms.Form):
    word = forms.CharField(label='Palabra', max_length=50, required=True)
