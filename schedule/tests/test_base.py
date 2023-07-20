from schedule.models import Appointment


def make_appointment(**kwargs) -> Appointment:
    new_appointment = Appointment.objects.create(
        category=kwargs.get('category', 'musculação'),
        date='2023-07-02 10:00',
        client_name=kwargs.get('client_name', 'jhon doe'),
        client_phone='123456789',
        description=kwargs.get('description', ''),
        feedback=kwargs.get('feedback', False),
    )
    new_appointment.save()
    return new_appointment


def make_appointment_range(quantity) -> None:
    for i in range(quantity):
        make_appointment()
