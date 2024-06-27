from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """Класс для формы регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ("email",)


class ProfileForm(forms.ModelForm):
    """Класс для формы профиля пользователя."""

    new_email = forms.EmailField(required=False, label="New Email")

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email", "new_email"]
        widgets = {
            "email": forms.TextInput(attrs={"readonly": True}),
        }

    def clean_new_email(self):
        """Проверка на уникальность нового email"""

        new_email = self.cleaned_data.get("new_email")
        if new_email and User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email is already in use.")
        return new_email
