from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('NotSay', 'NotSay'),
    ('Other', 'Other'),
)

YEAR_CHOICES = (
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
    ('5', '5th Year'),
    ('6', 'Graduated'),
    ('7', 'Faculty/Staff'),
    ('8', 'NA'),
)

class UserProfile(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='Email',default='testing_email')
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=100, default='fname')
    last_name = models.CharField(max_length=100, default='lname')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Gender', default='Male')
    contact = models.CharField(max_length=10, verbose_name='Contact')
    current_year = models.CharField(max_length=20, choices=YEAR_CHOICES, verbose_name='Current Year of Study', default='1')
    college = models.CharField(max_length=60, verbose_name='College Name')
    city = models.CharField(max_length=40, verbose_name='City')
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email