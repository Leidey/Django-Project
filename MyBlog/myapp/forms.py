from django.contrib.auth.models import User
from django import forms


from django.contrib.auth.forms import AuthenticationForm
from .models import Post


#from .models import SignUp

from django.utils.translation import ugettext_lazy as _



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",

        ]


# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#     ## exclude = ['full_name']
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         email_base, provider = email.split("@")
#         domain, extension = provider.split('.')
#         # if not domain == 'USC':
#         # 	raise forms.ValidationError("Please make sure you use your USC email.")
#         if not extension == "edu":
#             raise forms.ValidationError("Please use a valid .EDU email address")
#         return email
#
#     def clean_full_name(self):
#         full_name = self.cleaned_data.get('full_name')
#         # write validation code.
#         return full_name


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password(again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data



# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


