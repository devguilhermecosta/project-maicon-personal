# Generated by Django 4.1.7 on 2023-02-27 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_title', models.CharField(default='', max_length=255, verbose_name='título do perfil profissional')),
                ('profile_description', models.TextField(default='', max_length=255, verbose_name='descrição do perfil')),
                ('profile_image', models.ImageField(blank=True, default='', upload_to='app_home/images/profile/')),
            ],
        ),
        migrations.CreateModel(
            name='HomeContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_link', models.CharField(default='', max_length=255, verbose_name='link do instagram')),
                ('facebook_link', models.CharField(default='', max_length=255, verbose_name='link do facebook')),
                ('whatsapp_link', models.CharField(default='', max_length=255, verbose_name='link do whatsapp')),
                ('instagram_text', models.CharField(max_length=255, verbose_name='texto para o instagram')),
                ('facebook_text', models.CharField(max_length=255, verbose_name='texto para o facebook')),
                ('whatsapp_phone', models.CharField(max_length=255, verbose_name='número do whatsapp')),
                ('title_section_intro', models.CharField(default='', max_length=255, verbose_name='Título da seção inicial')),
                ('description_section_intro', models.TextField(default='', max_length=255, verbose_name='Descrição da seção intro')),
                ('subtitle_one_section_intro', models.CharField(default='', max_length=255, verbose_name='Primeiro Subtítulo')),
                ('sub_description_one_section_intro', models.TextField(default='', max_length=255, verbose_name='Primeira descrição')),
                ('subtitle_two_section_intro', models.CharField(default='', max_length=255, verbose_name='Segundo Subtítulo')),
                ('sub_description_two_section_intro', models.TextField(default='', max_length=255, verbose_name='Segunda descrição')),
                ('subtitle_three_section_intro', models.CharField(default='', max_length=255, verbose_name='Terceiro Subtítulo')),
                ('sub_description_three_section_intro', models.TextField(default='', max_length=255, verbose_name='Terceira descrição')),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_home.profile')),
            ],
        ),
    ]