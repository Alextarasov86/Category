# Generated by Django 4.1.3 on 2022-12-05 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
    ]
