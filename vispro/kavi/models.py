from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.text import slugify
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class kavi(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

class CustomUserManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)

class Auser(AbstractUser):
    phone_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        unique=True
    )
    email = models.EmailField(_('email address'), unique=True)
    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        STAFF = 'staff', _('Staff')
        USER = 'user', _('User')
        INACTIVE = 'inactive', _('Inactive')
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
            self.is_active = True

        elif self.role == self.Roles.STAFF:
            self.is_staff = True
            self.is_superuser = False
            self.is_active = True

        elif self.role == self.Roles.INACTIVE:
            self.is_active = False
            self.is_staff = False
            self.is_superuser = False

        else:
            self.is_staff = False
            self.is_superuser = False
            self.is_active = True

        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(Auser, on_delete=models.CASCADE)
    bio = models.TextField()
    city = models.CharField(max_length=100)

class BaseModel(models.Model):
    name = models.CharField(max_length=50, help_text='enter your name', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class category(BaseModel):

    def __str__(self):
        return self.name    
     
class movies(BaseModel):
    movie_charecter = models.CharField(max_length=50)
    movie_content = models.TextField()
    movie_image = models.ImageField(blank=True, upload_to='posts/images')
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(null=True, blank=True, unique=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1

            while movies.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


    @property
    def formatted_image(self):
        if not self.movie_image:
            return ""
        if str(self.movie_image).startswith(("http://", "https://")):
            return self.movie_image
        return self.movie_image.url

    
    def __str__(self):
        return str(self.name)
    
class Author(models.Model):
    name = models.CharField(max_length=50, default="vis")

STATUS_CHOICES = [
    ("A","very_like"),
    ("B","like"),
    ("C","ok"),
    ("D","bad"),
    ("E","very_bad")
]

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="C", null=True, blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="articles"
    )


    def __str__(self):
        return self.title

class mom_next_obj(models.QuerySet):
    def alive(self):
        return self.filter(is_alive=True)

    def high_salary(self):
        return self.filter(salary__gt=20000)

# class mom_obj(models.Manager.from_queryset(mom_next_obj)):

class mom_obj(models.Manager):
    def under18(self):
        return self.filter(age__lt=18)
    def under30(self):
        return self.filter(age__lt=30)
    def over18(self):
        return self.filter(age__gt=18)
    def over30(self):
        return self.filter(age__gt=30)

class Mom(BaseModel):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    initial = models.CharField(max_length=5, null=True, blank=True)
    age = models.IntegerField()
    salary = models.IntegerField()
    marrital_status = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)
    # objects = mom_next_obj.as_manager()
    objects = mom_obj()

    def __str__(self):
        return self.name or ""
    
    def fullname(self):
        last = self.last_name or ""
        return f"{self.first_name} {last}-{self.initial}"
    
class dad_obj(models.Manager):
    def under18(self):
        return self.filter(age__lt=18)
    def under30(self):
        return self.filter(age__lt=30)
    def over18(self):
        return self.filter(age__gt=18)
    def over30(self):
        return self.filter(age__gt=30)

class Dad(BaseModel):
    age = models.IntegerField()
    salary = models.IntegerField()
    marrital_status = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)
    objects = dad_obj

    def __str__(self):
        return self.name

STATUS = [
    ('D', 'Draft'),
    ('P', 'Published')
]

class LuckyNumber(models.IntegerChoices):
    ONE = 1, 'One'
    TWO = 2, 'Two'
    THREE = 3, 'Three'

class Active_Members(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    def over30(self):
        return self.filter(age__gt=30)
    def over18(self):
        return self.filter(age__gt=18)
    def under30(self):
        return self.filter(age__lt=30)
    def under18(self):
        return self.filter(age__lt=18)

class Vis_Members(BaseModel):
    age = models.PositiveIntegerField(help_text='enter your age', blank=True, null=True)
    lucky_number = models.IntegerField(choices=LuckyNumber.choices, help_text="select your lucky number")
    about = models.TextField(help_text='tell me about yourself', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web_site = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to= "posts/images", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    salary = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    sleeping_time = models.DurationField(blank=True, null=True)
    mother = models.ForeignKey(Mom, on_delete=models.CASCADE, related_name="amma")
    father = models.ForeignKey(Dad, on_delete=models.CASCADE, related_name="appa")
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="posts/files", blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique= True)
    data = models.JSONField(default=dict, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='D')
    objects = models.Manager()
    active = Active_Members()

    class Meta:
        ordering = ['age']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-age'])
        ]
        get_latest_by = 'created_at'
        db_table = 'vis_table'

    def clean(self):
        cleaned_data = super().clean()

        phone = self.phone
        email = self.email

        if phone and len(str(phone))!=10:
            raise ValidationError("phone numbers must 10 digits")
        
        if email and not email.endswith('@gmail.com'):
            raise ValidationError('email must end with @gmail.com')
    
    def created_duration(self):
        return timezone.now()-self.created_at
    
    def uploaded_duration(self):
        return timezone.now()-self.updated_at

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Vis_Members.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        if self.date_of_birth:
            today = datetime.date.today()  # Current date
            # Calculate age in years
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    # If name is NULL in the database → __str__() returns None → crash.
    
class Vis_Member_Created_Details(BaseModel):
    name = models.CharField(max_length=50)
    about_creation = models.TextField()

    def __str__(self):
        return self.name
    
