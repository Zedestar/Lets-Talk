from django import forms
from .models import Comment, Subscribe, Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Creating the forms here 

class CommentForm(forms.ModelForm):

    content = forms.CharField(
        label = 'Content',
        required =True,
        widget = forms.Textarea(
            attrs = {
                'placeholder':'Enter your comment content.....',
                'autocomplete':'off',
                'row':4
            }
        )
    )

    class Meta:
        model = Comment
        fields = {'content'}




class SubsribeForm(forms.ModelForm):
    email = forms.CharField(
        label = "",
        required = True,
        widget = forms.TextInput(
            attrs = {
                'autocomplete':'off',
                'placeholder':'Enter email to subscribe....'
            }
        )
    )
    class Meta:
        model = Subscribe
        fields = ('__all__')





class UserCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length = 3,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Enter Your user name...',
                'autocomplete':'off'
            }
        )
    )

    email = forms.CharField(
    min_length = 3,
    widget = forms.TextInput(
        attrs = {
            'placeholder':'Enter Your user email...',
            'autocomplete':'off'
        }
    )
    )

    password1 = forms.CharField(
    widget = forms.PasswordInput(
        attrs = {
            'placeholder':'Enter your password...',
            'autocomplete':'off'
        }
    )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name',)

    def clean_email(self):
        user_email = self.cleaned_data.get('email')
        if User.objects.filter(email = user_email).exists():
            raise ValidationError(f'The entered {user_email} email already exist, try another one')
        return user_email


      ######## FORM TO ADD POST ##########

class Create_Post(forms.ModelForm):
    title = forms.CharField(
    min_length = 3,
    max_length = 200,
    widget = forms.TextInput(
        attrs = {
            'placeholder':'Enter post title.....',
            'autocomplete':'off'
        }
    )
    )

    content = forms.CharField(
    min_length = 3,
    max_length = 200,
    widget = forms.Textarea(
        attrs = {
            'placeholder':'Enter Post content.....',
            'autocomplete':'off',
            'rows':'6'
        }
    )
    )

    slug = forms.CharField(
    min_length = 3,
    max_length = 200,
    widget = forms.TextInput(
        attrs = {
            'placeholder':'Youmay enter your name.....',
            'autocomplete':'off'
        }
    )
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'slug', 'image', 'tags')


class editProfile(forms.ModelForm):
    bio = forms.CharField(
    min_length = 3,
    max_length = 200,
    widget = forms.Textarea(
        attrs = {
            'placeholder':'Enter your bio.....',
            'autocomplete':'off'
        }
    )
    )
    class Meta:
        model = Profile
        fields = ('profile_image', 'bio',)