from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("correo_electronico", "nombre_de_usuario", "edad")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=(
            "correo_electronico","nombre_de_usuario","edad"
        )
