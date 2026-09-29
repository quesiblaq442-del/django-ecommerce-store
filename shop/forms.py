from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
