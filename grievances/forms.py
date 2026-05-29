from django import forms
from .models import Issue
from accounts.models import Municipality


class IssueReportForm(forms.ModelForm):
    latitude = forms.DecimalField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude = forms.DecimalField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Issue
        fields = [
            'title',
            'category',
            'description',
            'severity',
            'photo',
            'location_name',
            'municipality',
            'ward_number',
            'latitude',
            'longitude',
            'is_anonymous',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Large pothole near Koteshwor junction'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the issue in detail — size, danger level, how long it has been there...'
            }),
            'location_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Near Koteshwor petrol pump, opposite Nabil Bank'
            }),
            'ward_number': forms.NumberInput(attrs={
                'placeholder': 'e.g. 7',
                'min': 1,
                'max': 35
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.all().order_by('name')
        self.fields['municipality'].empty_label = "Select Municipality"
        self.fields['photo'].required = False
        self.fields['ward_number'].required = False
        self.fields['location_name'].required = False

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Photo must be under 10MB.")
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(photo, 'content_type') and photo.content_type not in allowed_types:
                raise forms.ValidationError("Only JPG, PNG, and WEBP photos allowed.")
        return photo