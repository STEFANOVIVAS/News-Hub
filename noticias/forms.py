from django import forms
from django.forms.widgets import Textarea


class ShareNoticiaForm(forms.Form):
    nome = forms.CharField(max_length=30)
    email = forms.EmailField()
    send_to = forms.EmailField()
    comentarios = forms.CharField(required=False, widget=Textarea)
