from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from .home_base_exception import ImageNotFoundError
from app_home import models as md


def __create_simple_image() -> SimpleUploadedFile:
    try:
        path: Path = Path(__file__).parent
        image_path: str = ''.join([str(path), '/images/profile.jpeg'])
        simple_image: SimpleUploadedFile = SimpleUploadedFile(
            name='image_profile',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg',
            )
    except FileNotFoundError:
        raise ImageNotFoundError(msg='Image not Found',
                                 path=image_path,
                                 )
    return simple_image


def make_social_network(instagram_link: str = 'instagram_link',
                        facebook_link: str = 'facebook_link',
                        whatsapp_link: str = 'whatsapp_link',
                        instagram_text: str = 'instagram_text',
                        facebook_text: str = 'facebook_text',
                        whatsapp_phone: str = 'whatsapp_phone',
                        ) -> md.SocialNetwork:

    data: dict = {
        'instagram_link': instagram_link,
        'facebook_link': facebook_link,
        'whatsapp_link': whatsapp_link,
        'instagram_text': instagram_text,
        'facebook_text': facebook_text,
        'whatsapp_phone': whatsapp_phone,
    }

    return md.SocialNetwork.objects.create(
        **data
    )


def make_section_intro(title: str = 'section_intro_title',
                       description: str = 'section_intro_description',
                       subtitle_one: str = 'subtitle_one',
                       sub_description_one: str = 'sub_description_one',
                       subtitle_two: str = 'section_intro_subtitle_two',
                       sub_description_two: str = 'sub_description_two',
                       subtitle_three: str = 'subtitle_three',
                       sub_description_three: str = 'sub_description_three',
                       ) -> md.SectionIntro:

    data: dict = {
        'title': title,
        'description': description,
        'subtitle_one': subtitle_one,
        'sub_description_one': sub_description_one,
        'subtitle_two': subtitle_two,
        'sub_description_two': sub_description_two,
        'subtitle_three': subtitle_three,
        'sub_description_three': sub_description_three,
    }

    return md.SectionIntro.objects.create(
        **data
    )


def make_profle(title: str = 'profile_title',
                description: str = 'profile_description',
                image: SimpleUploadedFile = __create_simple_image(),
                ) -> md.Profile:

    data: dict = {
        'title': title,
        'description': description,
        'image': image,
    }

    return md.Profile.objects.create(
        **data
    )


def make_pre_gallery(title: str = 'pre_gallery_title',
                     description: str = 'pre_gallery_description',
                     image_one: str = __create_simple_image(),
                     image_two: str = __create_simple_image(),
                     image_three: str = __create_simple_image(),
                     ) -> md.PreGallery:

    data: dict = {
        'title': title,
        'description': description,
        'image_one': image_one,
        'image_two': image_two,
        'image_three': image_three,
    }

    return md.PreGallery.objects.create(
        **data
    )


def make_adress(name: str = 'adress_name',
                adress: str = 'adress_adress',
                city: str = 'adress_city',
                postal: str = 'adress_postal',
                ) -> md.Adress:

    data: dict = {
        'name': name,
        'adress': adress,
        'city': city,
        'postal': postal,
    }

    return md.Adress.objects.create(
        **data
    )


def make_service(title: str = 'service_title',
                 description: str = 'service_description',
                 ) -> md.Service:

    data: dict = {
        'title': title,
        'description': description,
    }

    return md.Service.objects.create(
        **data
    )


def make_queryset_services(num_of_services: int) -> QuerySet[md.Service]:
    for i in range(num_of_services):
        make_service()

    return md.Service.objects.all()


def make_home_content() -> md.HomeContent:
    """return a complet instance of HomeContent"""
    home_content: md.HomeContent = md.HomeContent.objects.create(
        social_network=make_social_network(),
        section_intro=make_section_intro(),
        profile=make_profle(),
        pre_gallery=make_pre_gallery(),
        adress=make_adress(),
    )

    home_content.services.set(
        make_queryset_services(1)
    )

    return home_content
