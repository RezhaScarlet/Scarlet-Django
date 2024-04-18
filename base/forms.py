from django.forms import CharField, ModelForm, TextInput
from django.utils.text import slugify
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError('Room name must be at least 3 characters long.')
        return name

    # Add a custom validation method for security question (replace with your actual logic)
    def clean_security_answer(self):
        security_answer = self.cleaned_data['security_answer']
        if security_answer != 3 + 5:  # Replace with your desired validation logic
            raise ValidationError('Invalid security answer.')
        return security_answer

        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'bio']
        widgets = {
            'username': TextInput(attrs={'readonly': 'readonly'}),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}".strip()
        if commit:
            user.save()
        return user