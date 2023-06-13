from django.db import models
from django.core.validators import RegexValidator


class Vertical(models.Model):
    name = models.CharField(max_length=100)
    rank = models.IntegerField()  # for sorting

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vertical'
        verbose_name_plural = 'Verticals'


class CoreMember(models.Model):
    # Validator
    contact = RegexValidator(regex=r'^(\+91|0)?[6789]\d{9}$', message="Phone number must be entered in the format: '+91 9999999999'.")

    name = models.CharField(max_length=100)
    position = models.ForeignKey(Vertical, on_delete=models.CASCADE, related_name='new_position')
    image = models.ImageField(upload_to='images/coreteam/', default='https://as1.ftcdn.net/v2/jpg/03/46/83/96/1000_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, blank=True, validators=[contact])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Core Member'
        verbose_name_plural = 'Core Members'
