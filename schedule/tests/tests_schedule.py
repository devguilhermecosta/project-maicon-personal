from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from schedule.tests.test_base import make_appointment, make_appointment_range
from parameterized import parameterized
from unittest.mock import patch


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
        ('data e hora'),
        ('nome'),
        ('categoria'),
        ('feedback'),
        ('deletar'),
        ('02/07/2023 - 10:00'),
        ('jhon doe'),
        ('musculação'),
    ])
    def test_schedule_loads_correct_content(self, text: str) -> None:
        # make login
        self.make_login()

        # create the appointment
        make_appointment()

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
            'Nenhum agendamento até o momento',
            content,
        )

    def test_schedule_is_paginated(self) -> None:
        # create 100 appointments
        make_appointment_range(100)

        # make login
        self.make_login()

        # set the PER_PAGE with 10
        with patch('schedule.views.PER_PAGE', new=10):
            # make get request
            response = self.client.get(self.url)

            # get the context
            context = response.context

            # get the objects and paginatior
            appointments = context['objects']
            paginator = appointments.paginator

            self.assertEqual(paginator.num_pages, 10)
