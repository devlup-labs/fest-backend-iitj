from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


class Vertical(models.Model):
    name = models.CharField(max_length=100)
    rank = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vertical'
        verbose_name_plural = 'Verticals'


class CoreMember(models.Model):
    default_img = settings.DEFAULT_PROFILE_IMAGE_URL

    contact = RegexValidator(
        regex=r'^(\+91|0)?[6789]\d{9}$',
        message="Phone number must be in valid format."
    )

    name = models.CharField(max_length=100)
    position = models.ForeignKey(
        Vertical,
        on_delete=models.CASCADE,
        related_name='new_position'
    )
    image = models.ImageField(
        upload_to='images/coreteam/',
        default=default_img
    )
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, blank=True, validators=[contact])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Core Member'
        verbose_name_plural = 'Core Members'
