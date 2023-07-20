from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from schedule.models import Appointment
from parameterized import parameterized


class AppointmentTests(AuthorTestBase):
    url = reverse('schedule:appointment')

    def test_appointment_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/author/dashboard/agenda/novo_agendamento/',
        )

    def test_appointment_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.AppointmentView,
        )

    def test_appointment_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/author/login/?next=/author/dashboard/agenda/novo_agendamento/',
            302,
        )

    def test_appointment_returns_status_code_200_if_user_is_authenticated(self) -> None:   # noqa: E501
        # make login
        self.make_login()

        # make get request with user logged in
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_appointment_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        # make get request with user logged in
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'schedule/pages/new_appointment.html',
        )

    @parameterized.expand([
        ('categoria'),
        ('data e horário'),
        ('nome do aluno'),
        ('telefone'),
        ('observações'),
    ])
    def test_appointment_loads_correct_content(self, text: str) -> None:
        # make login
        self.make_login()

        # make get request with user logged in
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('category', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
        ('client_name', 'Campo obrigatório'),
        ('client_number', 'Campo obrigatório'),
    ])
    def test_appointment_returns_error_messages_if_required_fields_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # form data
        data = {
            field: '',
        }

        # make post request without required data
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertIn(
            'Existem campos obrigatórios',
            content,
        )
        self.assertRedirects(
            response,
            '/author/dashboard/agenda/novo_agendamento/',
            302,
        )

    def test_appointment_returns_success_message_if_the_appointment_is_created(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # form data
        data = {
            'category': 'eletro',
            'date': '2023-07-02 10:00',
            'client_name': 'jhon doe',
            'client_phone': '000000000',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Agendamente criado com sucesso',
            content,
            )
        self.assertRedirects(
            response,
            '/author/dashboard/agenda/',
            302,
        )

    def test_appointment_creates_a_new_object_if_success(self) -> None:
        # make login
        self.make_login()

        # form data
        data = {
            'category': 'eletro',
            'date': '2023-07-02 10:00',
            'client_name': 'jhon doe',
            'client_phone': '000000000',
        }

        # make post request
        self.client.post(
            self.url,
            data=data,
            follow=True,
            )

        # get object
        appointments = Appointment.objects.all()

        self.assertEqual(len(appointments), 1)
        self.assertEqual(
            appointments.first().client_name,
            'jhon doe',
        )
        self.fail('criar o teste de paginação')
