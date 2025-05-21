from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Имя пользователя",
        help_text="Обязательное поле. Не более 150 символов. "
        "Только буквы, цифры и символы @/./+/-/_",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        help_text="Ваш пароль должен содержать как минимум 3 символа."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        }),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_instance = getattr(self, "instance", None)

        if (
            user_instance
            and User.objects.filter(username=username)
            .exclude(pk=user_instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "Пользователь с таким логином уже существует."
            )
        elif (
            not user_instance
            and User.objects.filter(username=username).exists()
        ):
            raise forms.ValidationError(
                "Пользователь с таким логином уже существует."
            )

        return username
