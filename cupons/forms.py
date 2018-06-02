from django import forms


class CuponApllyForm(forms.Form):
    code = forms.CharField(label='Применить купон', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 200px'}))
