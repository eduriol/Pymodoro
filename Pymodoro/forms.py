from django import forms


class StartForm(forms.Form):
    tag = forms.CharField(max_length=200, error_messages={'required': '*',})