"""Celery tasks for the users app"""

from celery.schedules import crontab
from django.core.mail import send_mass_mail

from config.celery import celery_app
from config.settings.base import EMAIL_HOST_USER
from recipe.models import Recipe

from .models import CustomUser


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to test the celery worker"""
    print(f"Request: {self.request!r}")


@celery_app.task(bind=True, ignore_result=True)
def send_bulk_email_task(
    self,
):
    """Send an email to the recipients"""
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
        #  Load recipe data for the user
        recipe_likes = -1

        try:
            recipe_likes = Recipe.get_daily_likes(user)

        except Exception as e:
            print(f"An error occurred: {e}")

        data.append(
            (
                "Daily updates on your recipes!",
                f"Hello {user.username}, here are your daily updates on your recipes for today, Likes received: {recipe_likes} 👍🏼.",
                EMAIL_HOST_USER,
                [user.email],
            )
        )

    try:
        # pass

        # Using the send_mass_mail function to send bulk emails, reduces the number of open SMTP connections
        send_mass_mail(datatuple=data, fail_silently=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        return


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(hour=8, minute=0), # 8:00 AM everyday
            # 30.0, # 30 seconds for testing
            send_bulk_email_task.s(),
            name="send_email_everyday",
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return
