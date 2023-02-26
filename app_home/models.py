from django.db import models


class HomeContent(models.Model):
    instagram_link = models.CharField(max_length=255,
                                      blank=False,
                                      default='',
                                      verbose_name='link do instagram',
                                      )
    facebook_link = models.CharField(max_length=255,
                                     blank=False,
                                     default='',
                                     verbose_name='link do facebook',
                                     )
    whatsapp_link = models.CharField(max_length=255,
                                     blank=False,
                                     default='',
                                     verbose_name='link do whatsapp',
                                     )
    instagram_text = models.CharField(max_length=255,
                                      blank=False,
                                      verbose_name='texto para o instagram',
                                      )
    facebook_text = models.CharField(max_length=255,
                                     blank=False,
                                     verbose_name='texto para o facebook',
                                     )
    whatsapp_phone = models.CharField(max_length=255,
                                      blank=False,
                                      verbose_name='número do whatsapp',
                                      )
    title_section_intro = models.CharField(max_length=255,
                                           blank=False,
                                           default='',
                                           verbose_name='Título da seção inicial',
                                           )
    description_section_intro = models.TextField(max_length=255,
                                                 blank=False,
                                                 default='',
                                                 null=False,
                                                 verbose_name='Descrição da seção intro',
                                                 )
    subtitle_one_section_intro = models.CharField(max_length=255,
                                                  blank=False,
                                                  default='',
                                                  verbose_name='Primeiro Subtítulo',
                                                  )
    sub_description_one_section_intro = models.TextField(max_length=255,
                                                         blank=False,
                                                         default='',
                                                         null=False,
                                                         verbose_name='Primeira descrição',
                                                         )
    subtitle_two_section_intro = models.CharField(max_length=255,
                                                  blank=False,
                                                  default='',
                                                  verbose_name='Segundo Subtítulo',
                                                  )
    sub_description_two_section_intro = models.TextField(max_length=255,
                                                         blank=False,
                                                         default='',
                                                         null=False,
                                                         verbose_name='Segunda descrição',
                                                         )
    subtitle_three_section_intro = models.CharField(max_length=255,
                                                    blank=False,
                                                    default='',
                                                    verbose_name='Terceiro Subtítulo',
                                                    )
    sub_description_three_section_intro = models.TextField(max_length=255,
                                                           blank=False,
                                                           default='',
                                                           null=False,
                                                           verbose_name='Terceira descrição',
                                                           )

    def __str__(self):
        return 'Configuração da Home'
