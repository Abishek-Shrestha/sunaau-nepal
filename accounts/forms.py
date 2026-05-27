from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Municipality


class CitizenRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    municipality = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        required=False,
        empty_label="Select your Municipality"
    )
    ward_number = forms.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'municipality', 'ward_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citizen'
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.municipality = self.cleaned_data.get('municipality')
        user.ward_number = self.cleaned_data.get('ward_number')
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))