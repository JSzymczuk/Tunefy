from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, TextInput, PasswordInput, ModelForm, Form
from tunefy_cms.validators import validate_text_field


class LoginForm(Form):
    username = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Nazwa użytkownika'}))
    password = CharField(required=False, widget=PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean_username(self):
        validate_text_field(self, 'username', True, 20)
        value = self.cleaned_data.get('username')

        if User.objects.filter(username=value).first() is None:
            raise ValidationError(
                "Podany użytkownik nie istnieje.",
                code='invalid'
            )

        return value

    def clean_password(self):
        validate_text_field(self, 'password', True, 20, 6)

        password = self.cleaned_data.get('password')
        user = authenticate(username=self.cleaned_data.get('username'), password=password)

        if not user:
            raise ValidationError(
                "Podane hasło jest nieprawidłowe.",
                code='invalid'
            )

        return password


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Nazwa użytkownika'}),
            'password': PasswordInput(attrs={'placeholder': 'Hasło'})
        }

    password2 = CharField(required=False, widget=PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    def clean_username(self):
        validate_text_field(self, 'username', True, 20)
        value = self.cleaned_data.get('username')

        if User.objects.filter(username=value).first() is not None:
            raise ValidationError(
                "Podana nazwa użytkownika jest już zajęta.",
                code='invalid'
            )

        return value

    def clean_password(self):
        return validate_text_field(self, 'password', True, 20, 6)

    def clean_password2(self):
        validate_text_field(self, 'password2', True, 20)
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')

        if p1 != p2:
            raise ValidationError(
                "Podane hasła nie zgadzają się.",
                code='invalid'
            )

        return p2
