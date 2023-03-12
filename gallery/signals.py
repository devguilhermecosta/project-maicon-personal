import os

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from . models import Image


def delete_cover(instance: Image) -> None:
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Image)
def cover_delete(sender, instance: Image, *args, **kwargs) -> None:
    old_cover: Image = Image.objects.filter(id=instance.id).first()
    print('image deleted succesfully:', old_cover.cover.path)
    delete_cover(old_cover)


@receiver(pre_save, sender=Image)
def update_cover(sender, instance: Image, *args, **kwargs) -> None:
    try:
        old_instance: Image = Image.objects.filter(pk=instance.pk).first()
        new_instance: bool = old_instance.cover != instance.cover

        if new_instance:
            delete_cover(old_instance)
    except AttributeError:
        ...
