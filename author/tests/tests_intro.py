from . author_base_test import AuthorTestBase
from django.urls import reverse


class SectionIntroTests(AuthorTestBase):
    def test_intro_url_is_correct(self) -> None:
        url: str = reverse('author:sectionintro')

        self.assertEqual(
            '/author/dashboard/settings/sectionintro/edit/',
            url,
            )
        self.fail('continuer from here')
