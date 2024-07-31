from celery.schedules import crontab
from django.core.mail import send_mass_mail

from config.celery import celery_app
from config.settings.base import EMAIL_HOST_USER

from .models import CustomUser
from recipe.models import Recipe

# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to test the celery worker"""
    print(f"Request: {self.request!r}")


@celery_app.task(bind=True, ignore_result=True)
def send_bulk_email_task(self, ):
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

        # Import HTML template and load with user data
        # email_body: str = ""

        #  TODO: Fix the email template
        # try:
        #     email_body = render_to_string(
        #         template_name="daily-updates.html",
        #         context={
        #             "username": user.username,
        #             "recipe_likes": recipe_likes,
        #         },
        #     )

        #     email_body = strip_tags(email_body)
        # except Exception as e:
        #     print(f"An error occurred: {e}")


        data.append(
            (
                "Daily updates on your recipes!",
                f"Hello {user.username}, here are your daily updates on your recipes for today, Likes received: {recipe_likes} 👍🏼.",
                # email_body,
                EMAIL_HOST_USER,
                [user.email],
            )
        )
    
    try:
        # pass
        send_mass_mail(datatuple=data, fail_silently=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        return


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(hour=8, minute=0),
            # 30.0,
            send_bulk_email_task.s(),
            name="send_email_everyday",
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return
