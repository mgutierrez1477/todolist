from django.forms import ModelForm
from . models import Task
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Obtener el modelo User activo (puede ser el predeterminado o uno personalizado)
User = get_user_model()

class TaskForm(ModelForm):
    class Meta :
        
        model = Task
        
        fields = "__all__"
        
        exclude = ['creator']

        labels = {
            'users' : "Usuarios",
        }

        widgets = {
            'due_date': forms.DateInput(
                attrs={'type':'date'},
                format='%Y-%m-%d'
            )
        }
    

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text=''
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text='' 
    )

    class Meta :
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            'username': None,
        }