from django import forms
from django.contrib.auth.models import User
from django.forms.fields import DateField
from inventory.models import KBDocument, FinDocument
from teams.models import Teams
from common.models import Document
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')
class LoginForm(forms.ModelForm):
    user = forms.CharField(label='Username')
    pw = forms.CharField(widget=forms.PasswordInput(),label='Password')
    class Meta():
        model = User
        fields = ('username','password')

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


class DocumentForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        users = kwargs.pop('users', [])
        super(DocumentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['status'].choices = [
            (each[0], each[1]) for each in KBDocument.DOCUMENT_STATUS_CHOICE]
        self.fields['status'].required = False
        self.fields['title'].required = True
        if users:
            self.fields['shared_to'].queryset = users
        self.fields['shared_to'].required = False
        self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in Teams.objects.all().values('id', 'name')]
        self.fields["teams"].required = False

    class Meta:
        model = KBDocument
        fields = ['title', 'document_file', 'status', 'shared_to']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not self.instance.id:
            if KBDocument.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    'Document with this Title already exists')
                return title
        if KBDocument.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Document with this Title already exists')
            return title
        return title


class FinDocumentForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        users = kwargs.pop('users', [])
        super(FinDocumentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['status'].choices = [
            (each[0], each[1]) for each in FinDocument.DOCUMENT_STATUS_CHOICE]
        self.fields['status'].required = False
        self.fields['title'].required = True
        if users:
            self.fields['shared_to'].queryset = users
        self.fields['shared_to'].required = False
        self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in Teams.objects.all().values('id', 'name')]
        self.fields["teams"].required = False

    class Meta:
        model = FinDocument
        fields = ['title', 'document_file', 'status', 'shared_to']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not self.instance.id:
            if FinDocument.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    'Document with this Title already exists')
                return title
        if FinDocument.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Document with this Title already exists')
            return title
        return title
