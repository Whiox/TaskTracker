from django.forms import *
from authentication.models import User


class RegisterForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Пароли не совпадают")


class LoginForm(Form):
    username = CharField(max_length=63)
    password = CharField(widget=PasswordInput, max_length=63)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError("Неправильное имя пользователя")
        if not user.check_password(password):
            raise ValidationError("Неправильный пароль")
        self.user = user
        return self.cleaned_data
