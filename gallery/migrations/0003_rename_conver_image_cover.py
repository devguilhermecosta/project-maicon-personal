# Generated by Django 4.1.7 on 2023-03-03 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_remove_image_image_image_conver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='conver',
            new_name='cover',
        ),
    ]
