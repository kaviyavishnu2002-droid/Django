from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from datetime import datetime
from cbv.models import Detail, Age_Group, Item, Items, Book, Books
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from cbv import validaters
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeForm(forms.Form):
    name = forms.CharField(
        help_text='enter your correct name',
        required=True,
        max_length=50,
        label='name',
        widget=forms.TextInput(attrs={'placeholder':'enter your name',
                                      'title':'enter full name'
                                      ,'readonly':False})
    )
    age = forms.IntegerField(
        help_text='enter your correct age',
        widget=forms.NumberInput(attrs={'placeholder':'enter your age'})
    )
    marital_status = forms.BooleanField(
        help_text='enter your correct marital satatus',
        required=False,
        label='marital status',
        widget=forms.CheckboxInput()
    )
    date_of_birth = forms.DateField(
        help_text='enter your correct date of birth',
        label='date of birth',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data.get('name')
        age = self.cleaned_data.get('age')
        date_of_birth = self.cleaned_data.get('date_of_birth')

        if date_of_birth:
            today_year = datetime.now().year
            dob_age = today_year - date_of_birth.year
        else:
            dob_age = None

        if name and not name.endswith('nu'):
            raise ValidationError('Name must end with "nu"')

        if age and dob_age and age != dob_age:
            raise ValidationError('Your age and date of birth do not match')

        return cleaned_data

def custom_formfield_callback(db_field, **kwargs):
    formfield = db_field.formfield()
    if formfield and not isinstance(formfield.widget, forms.CheckboxInput):
        formfield.widget.attrs.setdefault(
            'placeholder', f'Enter {db_field.name}'
        )
    return formfield

class text(forms.TextInput):
    input_type = 'text' # or 'color

class Members_form(forms.ModelForm):
    name = forms.CharField(
        required=True,
        error_messages={
            'required':'name is required'
        },
        validators=[MinLengthValidator(5, 'must be 5 letters')],
        widget=text(attrs={'placeholder':'enter your full name'})
    )
    about = forms.CharField(required=False, help_text='it is optional')
    is_active = forms.BooleanField(required=False, help_text='it is optional but default is false')
    age_range = forms.ModelChoiceField(required=False, queryset=Age_Group.objects.none())
    #slug = forms.SlugField(required=False)
    #user = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    class Meta:
        model = Detail
        fields = ['name', 'age', 'about', 'age_range', 'phone', 'email_id', 'is_active']
        widgets = {
            'email_id':forms.EmailInput(
                attrs={
                    'placeholder':'enter your email address'
                }
            )
        }
        # exclude = ['created_at', 'updated_at']  (You must use either fields OR exclude, never both)
        # No validators option in Meta
        labels = {
            'name':"For Name",
            'age':'For Age',
            'phone':'For Phone'
        }
        help_texts = {
            'name':'enter your correct name',
            'age':'enter you correct age',
            'phone':'enter your phone numbers must be 10'
        }
        error_messages = {
            'email_id': {
                'required': 'Email is mandatory',
                'invalid': 'Enter a valid email'
            }
        }
        field_classes = {
            'email_id': forms.EmailField,
            'age': forms.IntegerField
        }
        # localized_fields = ['created_at']
        formfield_callback = custom_formfield_callback
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class','')
            field.widget.attrs['class'] = (f'{existing} form-control').strip()
            field.widget.attrs.setdefault('placeholder', field.label)
            self.fields['age_range'].queryset = Age_Group.objects.all()

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 0:
            raise forms.ValidationError("age must be positive integer")
        return age
    
    def clean_email_id(self):
        email = self.cleaned_data.get("email_id")
        if email and not email.endswith('@gmail.com'):
            raise ValidationError("email id end with must @gmail.com")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name and "@" in name:
            raise forms.ValidationError("name cannot contain '@'.")
        return cleaned_data
    # use- Meta.widgets,  Meta.labels, Meta.help_texts, Meta.error_messages

class AgeGroupForm(forms.ModelForm):
    age_groups = forms.CharField(required=True)

    class Meta:
        model = Age_Group
        fields = ['age_groups', 'about']

class Authentication_Form(AuthenticationForm):
    email = forms.CharField(
        help_text='username has must be within 10 letters',
        widget=forms.TextInput(attrs={
            'placeholder':'enter your email',
            'class': 'form-control',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    class Meta:
        model = User
        fields = ['email', 'password']

class Normal_LoginForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    class Meta:
        model = User
        fields = ['username', 'password']

class Usercreation_Form(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'enter your email address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('confirm_password',"password do not match")
        return cleaned_data
    
class Normal_Register_Form(forms.ModelForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'enter your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'enter your password again'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2',"password do not match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # ✅ HASH PASSWORD
        if commit:
            user.save()
        return user

    

class item_form(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class book_form(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class items_form(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'

class books_form(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

