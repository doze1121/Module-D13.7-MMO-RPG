from allauth.account.forms import LoginForm, SignupForm
from allauth.utils import get_username_max_length
from django import forms
from django.contrib.auth import get_user_model, login
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomLoginForm(LoginForm):
    password = CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "autocomplete": "current-password",
                "class": "form-control rounded-4"
            }
        )
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        login_widget = forms.TextInput(
            attrs={
                "placeholder": _("Username"),
                "autocomplete": "username",
                "class": "form-control rounded-4"
            },
        )
        login_field = forms.CharField(
            label=_("Username"),
            widget=login_widget,
            max_length=get_username_max_length(),
        )

        self.fields["login"] = login_field

    def clean_login(self):
        login_or_email = self.cleaned_data['login']
        if '@' in login_or_email:
            email = login_or_email
            login = None
        else:
            login = login_or_email
            email = None
        if login:
            if not User.objects.filter(username=login).first():
                raise forms.ValidationError('Такого имени пользователя не существует')
        elif email:
            if not User.objects.filter(email=email).first():
                raise forms.ValidationError('Пользователя с таким email не существует')
        return login_or_email

    def clean_password(self):
        password = self.cleaned_data['password']
        login_or_email = self.cleaned_data.get('login')

        if login_or_email:
            if '@' in login_or_email:
                if not User.objects.filter(email=login_or_email).first().check_password(password):
                    raise forms.ValidationError('Введен неверный пароль')
            else:
                if not User.objects.filter(username=login_or_email).first().check_password(password):
                    raise forms.ValidationError('Введен неверный пароль')

        return password


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields["password1"] = CharField(
            label=_("Password"),
            widget=forms.PasswordInput(attrs={
                "placeholder": _("Password"),
                'autocomplete': "new-password",
                'class': 'form-control rounded-4'
            })
        )

        self.fields['password2'] = CharField(
            label=_("Password (again)"),
            widget=forms.PasswordInput(attrs={
                "placeholder": _("Password (again)"),
                'class': 'form-control rounded-4'
            })
        )

        self.fields["username"] = forms.CharField(
            label=_("Username"),
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("Username"),
                    "autocomplete": "username",
                    "class": "form-control rounded-4"
                },
            ),
            max_length=get_username_max_length(),
        )

        self.fields["email"] = forms.CharField(
            label=_("E-mail address"),
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                    "class": "form-control rounded-4"
                },
            ),
            max_length=get_username_max_length(),
        )

    def clean_email(self):
        email = self.cleaned_data['email']

        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Неверный формат email адреса')
        elif User.objects.filter(email=email):
            raise forms.ValidationError('Такой адрес email уже существует')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data.get('email')

        if username == email:
            raise forms.ValidationError('Имя пользователя не может быть таким же как email адрес')
        elif User.objects.filter(username=username):
            raise forms.ValidationError('Такое имя пользователя уже существует')

        return username

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        elif password1.islower():
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        elif len(password1) < 8:
            raise forms.ValidationError('Пароль должен быть не короче 8-ми символов')

        return self.cleaned_data