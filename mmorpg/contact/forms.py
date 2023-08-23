from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email', )
        widgets = {
            'email': forms.TextInput(attrs={"class": "editContent", "placeholder": "Ваш Email..."})
        }
        labels = {
            'email': ''
        }
