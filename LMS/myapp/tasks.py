from apscheduler.schedulers.background import BackgroundScheduler
from .models import Employees


def increment_leave():
    employees = Employees.objects.all()
    for employee in employees:
        employee.balance += 2
        employee.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(increment_leave, 'cron', month='1', day='1', hour='0', minute='0')
    scheduler.start()
