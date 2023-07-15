from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

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

class User(AbstractUser):
    google_picture = models.TextField(default='', blank=True)
    is_google = models.BooleanField(default=False)
    profile_complete = models.BooleanField(default=False)
    iitj = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    # Validators
    valid_contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male'
    )
    contact = models.CharField(max_length=10, validators=[valid_contact])
    current_year = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES,
        default='1'
    )
    college = models.CharField(max_length=128)
    city = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
