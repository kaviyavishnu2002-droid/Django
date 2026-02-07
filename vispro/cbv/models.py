import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from . import validaters
from django.db.models import F
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Base_Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Age_Group(Base_Model):
    age_groups = models.CharField(max_length=50)
    about = models.CharField(max_length=100, null=True, blank= True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'age_group_table'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.age_groups)
            slug = base_slug
            counter = 1
            while Age_Group.objects.filter(slug = slug).exists():
                slug = f"{base_slug}-{counter}"
                counter +=1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.age_groups
    
def username_from_email(email):
    uname = email.split('@')[0]
    return uname

phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10-digit Indian phone number starting with 6,7,8, or 9."
)

def Email_validator(email):
    if not email.endswith('@gmail.com'):
        raise ValidationError('email is must be end with @gmail.com')

class Youngers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(age__lte =30)

class Middle_Agers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(age__gt = 30, age__lte = 70)

class Oldagers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(age__gt = 70)
    
class Active(models.Manager):
    def get_queryset(self):  # it's default
        return super().get_queryset().filter(is_active = True)
    def youngers(self):
        return self.filter(age__lte=30)
    def middelagers(self):
        return self.filter(age__gt=30, age__lte=80)
    def oldagers(self):
        return self.filter(age__gt=80)
    def agrade(self):
        return self.filter(grade = 'a')
 
class grades(models.QuerySet):
    def active(self):
        return self.filter(is_active = True)
    def inactive(self):
        return self.filter(is_active = False)
    def a_grade(self):
        return self.filter(grade = 'a')
    def b_grade(self):
        return self.filter(grade = 'b')
    def c_grade(self):
        return self.filter(grade = 'c')
    def d_grade(self):
        return self.filter(grade = 'd')

class Detail(Base_Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50, default=None,
        validators=[
            MaxLengthValidator(20),
            # RegexValidator(regex='^[a-zA-Z0-9_]+$',message='Only letters, numbers, and underscore allowed')
        ]
    )
    age = models.IntegerField()
    about = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_user', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    email_id = models.EmailField(validators=[Email_validator])
    is_active = models.BooleanField(default=True)
    age_range = models.ForeignKey("Age_Group", on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=50, null=True, blank=True)
    STATUS = [
        ('a', 'A grade'),
        ('b', 'B grade'),
        ('c', 'C grade'),
        ('d', 'D grade')
    ]
    grade = models.CharField(max_length=50, choices=STATUS, default='d',null=True, blank=True)
    # objects
    objects = models.Manager()
    youngers = Youngers()
    middeleagers = Middle_Agers()
    oldagers = Oldagers()
    active = Active()
    grades = grades.as_manager()

    class Meta:
        ordering = ['age', '-name']
        db_table = 'Members_Table'
        permissions = [
            ('can_publish_detail', 'Can publish detail'),
            ('can_approve_detail', 'Can approve detail'),
        ]
        get_latest_by = 'age'
        managed = True  # If False, Django will NOT create/migrate the table.

    def later_for_10years(self):
        return self.age+10
    
    def ageid(self):
        return Detail.objects.annotate(
            age_id = F('age')-F('id')
        )
    
    @classmethod
    def activecls(cls):
        return cls.objects.filter(is_active = True)
    
    @staticmethod
    def asumage(age):
        return age >= 30
    
    @property
    def validate_age(self):
        return 'Adult' if Detail.asumage(self.age) else 'Minor'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.name.lower().replace(" ",'-')
            slug = base_slug
            counter = 1
            while Detail.objects.filter(slug = slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.user_name and self.email_id:
            self.user_name = username_from_email(self.email_id)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class All_detail(Base_Model):
    detail = models.TextField()
    detail_time = models.DateTimeField(null=True, blank=True)

class Item(Base_Model):
    name = models.CharField(max_length=100)

class Book(Item):
    author = models.CharField(max_length=50)
    pages = models.IntegerField()
    price = models.IntegerField()

class ExpensiveBook(Book):
    class Meta:
        proxy = True
        ordering = ['-price']

    def is_expensive(self):
        return self.price > 500
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ExpensiveProduct(Product):
    class Meta:
        proxy = True
        ordering = ['-price']

    def is_expensive(self):
        return self.price > 1000

class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    initial = models.CharField(max_length=2, null=True, blank=True)

class Books(Item):
    author = models.CharField(max_length=50)
    pages = models.IntegerField()
