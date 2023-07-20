from django.urls import reverse, resolve
from author.tests.author_base_test import AuthorTestBase
from schedule import views
from schedule.models import Appointment
from schedule.tests.test_base import make_appointment


class AppointmenteFeedbackTests(AuthorTestBase):
    url = reverse('schedule:handle_feedback', args=(1,))

    def test_appointment_feedback_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/author/dashboard/agenda/agendamento/1/feedback/',
        )

    def test_appointment_feedback_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.AppointmentFeedbackView,
        )

    def test_appointment_returns_status_code_404_if_get_request(self) -> None:
        # make login
        self.make_login()

        # create the appointment
        make_appointment()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 404
        )

    def test_appointment_feedback_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without logged in
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            '/author/login/?next=/author/dashboard/agenda/agendamento/1/feedback/',  # noqa: E501
            302,
        )

    def test_appointment_feedback_returns_status_code_404_if_the_appointment_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without the appointment
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_appointment_feedback_changes_the_feedback_data_for_true_from_appointment(self) -> None:  # noqa: E501
        '''
            this test if the feedback attribute
            changes for True if this is False
        '''
        # make login
        self.make_login()

        # create the appointment
        ap = make_appointment()

        # checks feedback attribute before the request
        self.assertFalse(ap.feedback)

        # make post request
        self.client.post(self.url)

        # get the appointment
        appointment = Appointment.objects.get(pk=1)

        # checks if the appointment feedback is True
        self.assertTrue(appointment.feedback)

    def test_appointment_feedback_changes_the_feedback_data_for_false_from_appointment(self) -> None:  # noqa: E501
        '''
            this test if the feedback attribute
            changes for False if this is True
        '''
        # make login
        self.make_login()

        # create the appointment with feedback attribute as True
        ap = make_appointment(feedback=True)

        # checks feedback attribute before the request
        self.assertTrue(ap.feedback)

        # make post request
        self.client.post(self.url)

        # get the appointment
        appointment = Appointment.objects.get(pk=1)

        # checks if the appointment feedback is False
        self.assertFalse(appointment.feedback)
