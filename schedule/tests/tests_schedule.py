from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from parameterized import parameterized


class ScheduleTests(AuthorTestBase):
    url = reverse('schedule:schedule')

    def test_schedule_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/author/dashboard/agenda/',
        )

    def test_schedule_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.SheduleView,
        )

    def test_schedule_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/author/login/?next=/author/dashboard/agenda/',
            302,
        )

    def test_schedule_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('data'),
        ('nome'),
        ('categoria'),
        ('feedback'),
        ('guilherme costa'),
        ('02/07/2023'),
        ('eletro'),
        ('não')
    ])
    def test_schedule_loads_correct_content(self, text: str) -> None:
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_schedule_loads_no_engagement_so_far(self) -> None:
        # make login
        self.make_login()

        # make get request without task
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'nenhum agendamento até o momento',
            content,
        )
