import posixpath
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from django import forms
from django.forms import ModelForm, TextInput, ValidationError

from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from Auth.models import SocialPerson

def thumbnail(image_path, width, height):
    absolute_url = posixpath.join(settings.MEDIA_URL, image_path)
    return f'<img src="{absolute_url}" alt="{image_path}" class="django-widget-img" ' \
           f'width={width} height={height} loading=lazy />', absolute_url

class ImageWidget(forms.ClearableFileInput):
    template = """<div style="display:flex; flex-direction:column;">
               <div>%(input)s</div><div class="margin-top:1rem;">
               <a href="%(image_url)s" target=_blank>%(image)s</a>
               </div></div>"""
    template_name = 'admin/widgets/clearable_file_input.html'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        if not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
            substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
            substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})

        input_html = super().render(name, value, attrs)
        if value and hasattr(value, 'width') and hasattr(value, 'height'):
            image_html, image_url = thumbnail(value.name, self.width, self.height)
            output = self.template % {'input': input_html,
                                      'image': image_html,
                                      'image_url': image_url}
        else:
            output = input_html
        return mark_safe(output)

class EditImage(ModelForm):
    class Meta:
        model = SocialPerson
        fields = [
            'info', 
            'job', 
            'age', 
            'phone', 
            'address', 
            'photo', 
            'back', 
            'instagram', 
            'facebook', 
            'github', 
            'twitter']
        # exclude = ['user', 'slug']
        labels = {
            'back':'Background photo'
        }
        widgets = {
            'photo': ImageWidget,
            'back': ImageWidget,
            'info' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'job' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'age' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'phone' : forms.TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'address' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'facebook' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'instagram' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'twitter' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            }),
            'github' : TextInput(attrs={
                'class':"form-control",
                'type':"text"
            })
        }
    def clean_age(self):
        age = self.cleaned_data['age']
        if age > 89:
            raise forms.ValidationError('Котагым жемей дурыс жасынды жаз!')
        return age
        

class EditProfileForm(ModelForm):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

        labels = {
            'first_name': 'First Name:',
            'last_name': 'Second Name:',
            'email': 'Email: '
        }

        email = forms.EmailField()

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type':'text'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            })
        }
    