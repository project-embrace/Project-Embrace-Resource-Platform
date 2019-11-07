from django import forms
from django.contrib.auth.models import User
from django.forms.fields import DateField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ExampleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Submit'))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class OutreachForm(forms.Form):
     first_name = forms.CharField(label='First Name',max_length=20)
     last_name = forms.CharField(label='Last Name',max_length=20,)
     email = forms.EmailField(label='Email')
     organization = forms.CharField(label='Organization',max_length=60)
     region = forms.CharField(label='Region',max_length=60)
     country = forms.CharField(label='Country',max_length=60)
     notes = forms.CharField(label='Notes',max_length=470,widget=forms.Textarea)
     def __init__(self, *args, **kwargs):
         super(OutreachForm, self).__init__(*args, **kwargs)
         self.helper = FormHelper()
         self.form_class = 'form-horizontal'
         self.label_class = 'col-lg-2'
         self.field_class = 'col-lg-8'

         self.helper.add_input(Submit('submit', 'Submit'))
