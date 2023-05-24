import json
import mimetypes

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User, Video, Comments

user = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UserChangeForm(UserChangeForm):
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label='День рождения'
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('name', 'email', "birthday")

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }