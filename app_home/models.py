from django.db import models


class SocialNetwork(models.Model):
    instagram_link = models.CharField(max_length=255,
                                      default='',
                                      verbose_name='link do instagram',
                                      )
    facebook_link = models.CharField(max_length=255,
                                     default='',
                                     verbose_name='link do facebook',
                                     )
    whatsapp_link = models.CharField(max_length=255,
                                     default='',
                                     verbose_name='link do whatsapp',
                                     )
    instagram_text = models.CharField(max_length=255,
                                      verbose_name=('texto para o botão'
                                                    ' do instagram'),
                                      )
    facebook_text = models.CharField(max_length=255,
                                     verbose_name=('texto para o botão'
                                                   ' do facebook'),
                                     )
    whatsapp_phone = models.CharField(max_length=255,
                                      verbose_name='número do whatsapp',
                                      )

    def __str__(self) -> str:
        return 'Configurar as redes sociais'

    class Meta:
        verbose_name = 'Redes Sociais'
        verbose_name_plural = 'Redes Sociais'


class SectionIntro(models.Model):
    title = models.CharField(max_length=255,
                             default='',
                             verbose_name='Título',
                             )
    description = models.TextField(max_length=500,
                                   default='',
                                   verbose_name='Descrição',
                                   )
    subtitle_one = models.CharField(max_length=255,
                                    default='',
                                    verbose_name='Primeiro Subtítulo',
                                    )
    sub_description_one = models.TextField(max_length=255,
                                           default='',
                                           verbose_name='Primeira descrição',
                                           )
    subtitle_two = models.CharField(max_length=255,
                                    default='',
                                    verbose_name='Segundo Subtítulo',
                                    )
    sub_description_two = models.TextField(max_length=255,
                                           default='',
                                           verbose_name='Segunda descrição',
                                           )
    subtitle_three = models.CharField(max_length=255,
                                      default='',
                                      verbose_name='Terceiro Subtítulo',
                                      )
    sub_description_three = models.TextField(max_length=255,
                                             default='',
                                             verbose_name='Terceira descrição',
                                             )

    def __str__(self) -> str:
        return 'Configurar a seção intro'

    class Meta:
        verbose_name = 'Seção de introdução'
        verbose_name_plural = 'Seção de introdução'


class Profile(models.Model):
    title = models.CharField(max_length=255,
                             default='',
                             verbose_name='título',
                             )
    description = models.TextField(max_length=500,
                                   default='',
                                   verbose_name='descrição',
                                   )
    image = models.ImageField(upload_to='app_home/images/profile/',
                              blank=True,
                              default='',
                              verbose_name='Imagem',
                              )

    def __str__(self) -> str:
        return 'Configurar o perfil profissional'

    class Meta:
        verbose_name = 'Perfil do Profissional'
        verbose_name_plural = 'Perfil do Profissional'


class PreGallery(models.Model):
    local = 'app_home/images/pre-gallery'

    title = models.CharField(max_length=255,
                             default='',
                             verbose_name='título',
                             )
    description = models.TextField(max_length=500,
                                   default='',
                                   verbose_name='descrição',
                                   )
    image_one = models.ImageField(upload_to=local,
                                  default='',
                                  verbose_name='primeira imagem',
                                  )
    image_two = models.ImageField(upload_to=local,
                                  default='',
                                  verbose_name='segunda imagem',
                                  )
    image_three = models.ImageField(upload_to=local,
                                    default='',
                                    verbose_name='terceira imagem',
                                    )

    def __str__(self) -> str:
        return 'Configurar a galeria de imagens da home'

    class Meta:
        verbose_name = 'Galeria de imagens da home'
        verbose_name_plural = 'Galeria de imagens da home'


class Service(models.Model):
    title = models.CharField(max_length=255,
                             default='',
                             verbose_name='título',
                             )
    description = models.TextField(max_length=255,
                                   default='',
                                   verbose_name='descrição',
                                   )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Serviços'
        verbose_name_plural = 'Serviços'


class Adress(models.Model):
    name = models.CharField(max_length=255,
                            default='',
                            verbose_name='nome do estabelecimento',
                            )
    adress = models.CharField(max_length=255,
                              default='',
                              verbose_name='endereço',
                              )
    city = models.CharField(max_length=255,
                            default='',
                            verbose_name='bairro e cidade',
                            )
    postal = models.CharField(max_length=255,
                              default='',
                              verbose_name='cep',
                              )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereço'


class HomeContent(models.Model):
    social_network = models.ForeignKey(SocialNetwork,
                                       on_delete=models.CASCADE,
                                       default=None,
                                       verbose_name='redes sociais',
                                       )

    section_intro = models.ForeignKey(SectionIntro,
                                      on_delete=models.CASCADE,
                                      default=None,
                                      verbose_name='seção intro',
                                      )

    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                default=None,
                                verbose_name='perfil do profissional',
                                )

    pre_gallery = models.ForeignKey(PreGallery,
                                    on_delete=models.CASCADE,
                                    default=None,
                                    verbose_name='galeria de imagens',
                                    )

    services = models.ManyToManyField(Service,
                                      verbose_name='serviços',
                                      )

    adress = models.ForeignKey(Adress,
                               on_delete=models.CASCADE,
                               default=None,
                               verbose_name='endereço',
                               )

    is_home = models.BooleanField(verbose_name='is_home',
                                  default=True,
                                  )

    def __str__(self):
        return 'Configuração da Home'

    class Meta:
        verbose_name = 'Todas as configurações do site'
        verbose_name_plural = 'Todas as configurações do site'
