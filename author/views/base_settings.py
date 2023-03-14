from app_home.models import HomeContent


def home_content() -> HomeContent:
    return HomeContent.objects.first()
