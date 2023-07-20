from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from schedule.models import Appointment
from schedule.tests.test_base import make_appointment


class AppointmentDeleteTests(AuthorTestBase):
    url = reverse('schedule:appointment_delete', args=(1,))

    def test_appointment_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/author/dashboard/agenda/agendamento/1/deletar/',
        )

    def test_appointment_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.AppointmentDeleteView,
        )

    def test_appointment_delete_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/author/login/?next=/author/dashboard/agenda/agendamento/1/deletar/',  # noqa: E501
            302,
        )

    def test_appointment_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the appointment
        make_appointment()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_appointment_delete_returns_status_code_404_if_the_appointment_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request with a non-existent appointment
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_appointment_delete_remove_the_appointment_from_database(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the appointment
        make_appointment()

        # checks if the appointment has been created
        ap_checks = Appointment.objects.all()
        self.assertEqual(len(ap_checks), 1)

        # make post request
        self.client.post(self.url)

        # get again the appointment
        appointments = Appointment.objects.all()

        # checks if the appointment has been deleted
        self.assertEqual(len(appointments), 0)
