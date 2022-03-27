from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm,
    # ReadOnlyPasswordHashField
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


### Following forms will be used in the admin site.  ###
class AdminUserCreationForm(BaseUserCreationForm):
    class Meta:
        model 	= User
        fields 	= '__all__'


class AdminUserChangeForm(BaseUserChangeForm):
    class Meta:
        model 	= User
        fields 	= '__all__'


### Following forms will be used in the main site.  ###
class UserCreationForm(BaseUserCreationForm):
    # set password2 to None to override parent class field
    password2 = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        labels = {
            'email': _('Email address')
        }

    ## No need for this since form won't be handled by django
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Remove autofocus set by superclass on `username_field` (email)
    #     self.fields['email'].widget.attrs.pop('autofocus')

    #     # Set class on password field
    #     # this can't be done on the Meta.widgets object because
    #     # this field was set in the class definition(super class)
    #     self.fields['password1'].widget.attrs.update({'class': 'js-password1'})

    def _post_clean(self):
        super()._post_clean()

        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password1')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user
    
    
