from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255,
                             blank=True,
                             default='',
                             verbose_name='título',
                             )
    description = models.TextField(max_length=500,
                                   blank=True,
                                   default='',
                                   verbose_name='descrição',
                                   )
    image = models.ImageField(upload_to='gallery/%Y/%m/',
                              verbose_name='imagem',
                              )

    def __str__(self):
        name = self.image.name.strip()

        return name[16:]

    class Meta:
        verbose_name = 'imagem'
        verbose_name_plural = 'imagens'
