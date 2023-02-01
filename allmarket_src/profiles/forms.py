from django import forms
from allauth.account.forms import SignupForm

from .models import MarketingPreference



class SignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name  = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

        
class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model  = MarketingPreference
        fields = ['subscribed']

