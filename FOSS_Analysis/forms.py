from django import forms

class urlForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(attrs={
        'id': 'github-url',
        'placeholder': 'Type your Github project url here',
        'max_length': 100
    }))
