from django.db import models


class Sponsor(models.Model):
    sponsor_image = models.ImageField(upload_to="sponsors")
    sponsor_name = models.CharField(max_length=50)
    sponsor_link = models.URLField(max_length=255)
    is_old = models.BooleanField(default=False)

    class Meta:
        app_label = 'sponsors'

    def __str__(self):
        return self.sponsor_name
