# from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from .models import Message, Profile, Skill


class CustomUserCreationForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2', ]
        labels = {
            'first_name':'Name',
        }
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForms, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'location', 'email', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_instagram', 'social_twitter', 'social_website', 'social_linkedin']
        labels = {
            'short_intro': 'Intro',
            'social_website': 'Website',
            'social_twitter': 'Twitter',
            'social_instagram': 'Instagram',
            'social_linkedin': 'LinkedIn',
            'social_github': 'GitHub',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class AddSkillsForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(AddSkillsForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class EditSkillsForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(EditSkillsForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    
    
