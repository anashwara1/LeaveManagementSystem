from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from django.apps import apps
from django.core.mail import send_mail


def increment_leave():
    try:
        LeaveBalance = apps.get_model('leaves', 'LeaveBalance')
        leaves = LeaveBalance.objects.all().distinct()

        for leave in leaves:
            leave.leave_earned += int(config('leave_increment'))
            leave.save()

    except Exception as e:
        subject = 'LEAVE INCREMENT FUNCTION NOT EXECUTED'
        message = f'The leave increment was not executed this month due to the following error.  {e}'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [from_email]

        send_mail(subject, message, from_email, recipient_list)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(increment_leave, 'cron', month='*', day='1', hour='0', minute='0')
    scheduler.start()
