# Generated by Django 4.2 on 2023-04-18 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_image', models.ImageField(upload_to='sponsors')),
                ('sponsor_name', models.CharField(max_length=50)),
                ('sponsor_link', models.URLField(max_length=255)),
                ('is_old', models.BooleanField(default=False)),
            ],
        ),
    ]
