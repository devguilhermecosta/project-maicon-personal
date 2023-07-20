# Generated by Django 4.1.7 on 2023-07-18 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_home', '0005_alter_socialnetwork_facebook_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_link',
            field=models.CharField(default='', max_length=255, verbose_name='link do facebook'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='facebook_text',
            field=models.CharField(default='', max_length=255, verbose_name='texto para o botão do facebook'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_link',
            field=models.CharField(default='', max_length=255, verbose_name='link do instagram'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='instagram_text',
            field=models.CharField(default='', max_length=255, verbose_name='texto para o botão do instagram'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='whatsapp_link',
            field=models.CharField(default='', max_length=255, verbose_name='link do whatsapp'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='whatsapp_phone',
            field=models.CharField(default='', max_length=255, verbose_name='número do whatsapp'),
        ),
    ]