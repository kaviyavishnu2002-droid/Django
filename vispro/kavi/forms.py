from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, authenticate
from .models import movies,category, Vis_Members, Mom, Dad
from django.contrib.auth import get_user_model

User = get_user_model()

class Vis_Member_Form(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':"enter your name"}))
    date_of_birth = forms.DateField(required=False,
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    input_formats=['%Y-%m-%d', '%d-%m-%Y'])
    age = forms.IntegerField(required=False)
    slug = forms.SlugField(required=False)
    
    class Meta:
        model = Vis_Members
        fields = "__all__"
        exclude = ['slug', 'data']

class Mom_create_Form(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    initial = forms.CharField(required=True)
    class Meta:
        model = Mom
        fields = ['first_name', 'last_name', 'initial', 'age', 'salary', 'marrital_status', 'is_alive']

class Dad_Create_Form(forms.ModelForm):
    class Meta:
        model = Dad
        fields = '__all__'

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=50, required=True, widget= forms.TextInput(attrs = {'placeholder': 'enter username'}))
    first_name = forms.CharField(label='First Name', max_length=50, required=True, widget= forms.TextInput(attrs = {'placeholder': 'enter your first name'}))
    email = forms.EmailField(label='Email', max_length=50, required=True, widget= forms.EmailInput(attrs = {'placeholder': 'enter your email'}))
    last_name = forms.CharField(label='Last Name', max_length=50, required=True, widget= forms.TextInput(attrs = {'placeholder': 'enter your last name'}))
    password = forms.CharField(label='Password', max_length=50, required=True, widget= forms.PasswordInput(attrs = {'placeholder': 'enter password'}))
    confirm_password = forms.CharField(label='Confirm password', max_length=50, required=True, widget= forms.PasswordInput(attrs = {'placeholder': 'enter confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password']

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")

        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError("Passwords does not match")

        return cleaned_data
    
class loginform(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=50, required=True, 
                               widget= forms.TextInput(attrs = {'placeholder': 'enter username'}))
    password = forms.CharField(label='Password', max_length=50, required=True, 
                               widget= forms.PasswordInput(attrs = {'placeholder': 'enter password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('invalid username and password')
            
class logout():
    pass

class add_category_form(forms.ModelForm):
    name = forms.CharField(max_length=50)
    
    class Meta:
        model = category
        fields = ['name']

class add_moviesform(forms.ModelForm):
    movie_name = forms.CharField(max_length=50, min_length=3, required=True, label='movie_name',
                                  widget= forms.TextInput(attrs = {'placeholder': 'enter movie name'}))
    movie_charecter = forms.CharField(required=True, label='movie_charecter',
                                  widget= forms.TextInput(attrs = {'placeholder': 'enter movie charecter name'}))
    movie_content = forms.CharField(required=True, label='movie_content',
                                  widget= forms.Textarea(attrs = {'placeholder': 'enter movie content'}))
    movie_image = forms.ImageField(required=False, label='movie_image',
                                  widget= forms.FileInput(attrs = {'placeholder': 'enter movie image url'}))
    category = forms.ModelChoiceField(queryset=category.objects.all(), label='category', required=False)
    is_published = forms.BooleanField(required=False, label='is published', widget=forms.CheckboxInput)
    
    class Meta:
        model = movies
        fields = ['movie_name','movie_charecter', 'movie_content', 'movie_image', 'category', 'is_published']

    def save(self, commit = True):
        post = super().save(commit=False)

        if self.cleaned_data.get('movie_image'):
            post.movie_image = self.cleaned_data.get('movie_image')

        else:
            movie_image = "posts/images/vishnu_zHTHXr8.jpg"
            post.movie_image = movie_image
        
        if commit:
            post.save()
        return post
    
    def clean(self):
        return super().clean()

class forgot_passwordform(forms.Form):
    email = forms.EmailField(label= 'email', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists:
            raise forms.ValidationError('email do not exists')