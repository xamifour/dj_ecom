from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class CustomProcessAdapter(DefaultAccountAdapter):

    def clean_username(self, username):
        if len(username) > 8:
            raise ValidationError('Please enter a username value less than the current one')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.

    def clean_email(self,email):
        RestrictedList = ['xamifour@gmail2.com']
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.')
        return email

    def clean_password(self,password):
    	if len(password) > 20:
    		raise ValidationError('Please Enter a password not more than 20')
    	return DefaultAccountAdapter.clean_password(self,password)