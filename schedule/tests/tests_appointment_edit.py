from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from schedule.models import Appointment
from schedule.tests.test_base import make_appointment
from parameterized import parameterized


class AppointmentEditTests(AuthorTestBase):
    url = reverse('schedule:appointment_edit', args=(1,))

    def test_appointmente_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/author/dashboard/agenda/agendamento/1/editar/',
            )

    def test_appointment_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.AppointmentEditView,
        )

    def test_appointment_edit_is_not_allowed_if_uses_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without login
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/author/login/?next=/author/dashboard/agenda/agendamento/1/editar/',  # noqa: E501
            302,
        )

    def test_appointment_edit_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new appointment
        make_appointment()

        # get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_appointment_edit_returns_status_code_404_if_the_appointment_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request without login
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_appointment_edit_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new appointment
        make_appointment()

        # get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'schedule/pages/new_appointment.html',
        )

    @parameterized.expand([
        ('category', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
        ('client_name', 'Campo obrigatório'),
        ('client_phone', 'Campo obrigatório'),
    ])
    def test_appointment_edit_returns_error_messages_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the new appointment
        make_appointment()

        # data
        data = {
            field: '',
        }

        # make post request without data
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            msg,
            content,
        )
        self.assertRedirects(
            response,
            '/author/dashboard/agenda/agendamento/1/editar/',
            302,
        )

    def test_appointment_edit_returns_success_message_if_form_is_ok(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the new appointment
        make_appointment()

        # data
        data = {
            'category': 'musculação',
            'date': '2023-08-10 14:00',
            'client_name': 'jhon another doe',
            'client_phone': '+55 9 89653256',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Agendamento alterado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/author/dashboard/agenda/',
            302,
        )

    def test_appointment_edit_modify_the_appointment_data(self) -> None:
        # make login
        self.make_login()

        # create the new appointment
        make_appointment()

        # data
        data = {
            'category': 'musculação',
            'date': '2023-08-10 14:00',
            'client_name': 'jhon another doe',
            'client_phone': '+55 9 89653256',
        }

        # make post request
        self.client.post(
            self.url,
            data=data,
            follow=True,
        )

        # get the appointment object
        appointment = Appointment.objects.get(pk=1)

        self.assertEqual(appointment.category, data['category'])
        self.assertEqual(appointment.client_name, data['client_name'])
        self.assertEqual(appointment.client_phone, data['client_phone'])
