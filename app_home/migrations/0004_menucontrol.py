# Generated by Django 4.1.7 on 2023-03-12 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_home', '0003_remove_homecontent_is_home'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_home', models.BooleanField(default=True)),
            ],
        ),
    ]