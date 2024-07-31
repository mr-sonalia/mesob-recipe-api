from celery.schedules import crontab
from django.core.mail import send_mass_mail

from config.celery import celery_app
from config.settings.base import EMAIL_HOST_USER

from .models import CustomUser


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to test the celery worker"""
    print(f"Request: {self.request!r}")


@celery_app.task(bind=True, ignore_result=True)
def send_bulk_email_task(self, data: list[tuple[str, str, str, list[str]]]):
    """Send an email to the recipients"""

    #  Create a new file using the open() function
    #  and write the email content to the file
    #  using the write() function
    #  Finally, close the file using the close() function
    #  and return the file path

    open("email.txt", "w").write(data)
    

    try:
        send_mass_mail(datatuple=data, fail_silently=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        return


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    users = []
    data: list[tuple[str, str, str, list[str]]] = []

    try:
        users = CustomUser.objects.all()
    except CustomUser.DoesNotExist:
        print("No users found")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    for user in users:
        data.append(
            (
                "Subject",
                "Message",
                EMAIL_HOST_USER,
                [user.email],
            )
        )
    try:

        sender.add_periodic_task(
            # crontab(minute="*/1"),
            30.0,
            send_bulk_email_task.s(data),
            name="send_email_everyday",
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return
