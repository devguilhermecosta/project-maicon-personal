import os
from django.db import models
from project.settings import MEDIA_ROOT
from PIL import Image as img


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

    @staticmethod
    def resize_image(image, new_width) -> None:
        full_path: str = os.path.join(MEDIA_ROOT, image.name)
        pillow_image = img.open(full_path)
        width, height = pillow_image.size

        if width > new_width:
            new_height = round((new_width * height) / width)
            pillow_image.resize((new_width, new_height),
                                img.LANCZOS)
            pillow_image.save(full_path,
                              optimize=True,
                              )

    def save(self, *args, **kwargs) -> None:
        super_save = super().save(*args, **kwargs)

        if self.image:
            try:
                self.resize_image(self.image, 840)
                print('resized image succesfully')
            except FileNotFoundError:
                ...

        return super_save

    class Meta:
        verbose_name = 'imagem'
        verbose_name_plural = 'imagens'
