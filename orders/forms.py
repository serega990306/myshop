from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'country', 'state', 'city', 'street', 'home', 'appartment', 'index',
                  'phone_number']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            'country': forms.TextInput(attrs={'class': 'form-control', }),
            'state': forms.TextInput(attrs={'class': 'form-control', }),
            'city': forms.TextInput(attrs={'class': 'form-control', }),
            'street': forms.TextInput(attrs={'class': 'form-control', }),
            'home': forms.TextInput(attrs={'class': 'form-control', }),
            'appartment': forms.TextInput(attrs={'class': 'form-control', }),
            'index': forms.TextInput(attrs={'class': 'form-control', }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', }),
        }
