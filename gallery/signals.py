import os

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from . models import Image


def delete_cover(instance: Image) -> None:
    try:
        os.remove(instance.image.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance: Image, *args, **kwargs) -> None:
    old_image: Image = Image.objects.filter(pk=instance.pk).first()
    delete_cover(old_image)


@receiver(pre_save, sender=Image)
def update_image(sender, instance: Image, *args, **kwargs) -> None:
    old_instance: Image = Image.objects.filter(id=instance.id).first()
    try:
        new_instance: bool = old_instance.image.path != instance.image.path
    except AttributeError:
        print('aquie é old path:', old_instance)

    if new_instance:
        delete_cover(old_instance)
