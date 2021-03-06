from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from apps.account.models import CustomUser
from apps.blog.models import Post


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Your Username", 'class': 'form-control', }))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': "Your Email", 'class': 'form-control  mt-4', }))

    password1 = forms.CharField(
        label=_("Password:"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': "Password",
            'class': 'form-control  mt-4',
        }),
        # help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': "Repeat your password ",
            'class': 'form-control  mt-4',
        }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'approved', 'approved_by', 'published', 'draft')






