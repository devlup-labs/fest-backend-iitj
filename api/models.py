from django.db import models

class Verticles(models.Model):
    name = models.CharField(max_length=100, verbose_name='Verticle Name', blank=False, null=False)
    rank = models.IntegerField(verbose_name='Verticle Rank', blank=False, null=False)  # for sorting

    def __str__(self):
        return self.name


class CoreTeam(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', blank=False, null=False)
    position = models.ForeignKey(Verticles, on_delete=models.CASCADE, verbose_name='Position')
    image = models.ImageField(upload_to='images/coreteam/', verbose_name='Image', default='https://as1.ftcdn.net/v2/jpg/03/46/83/96/1000_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')
    email = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
