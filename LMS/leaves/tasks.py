from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps


def increment_leave():
    Employees = apps.get_model('leaves', 'Employees')
    employees = Employees.objects.all()
    for employee in employees:
        employee.balance += 2
        employee.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(increment_leave, 'cron', month='1', day='1', hour='0', minute='0')
    scheduler.start()
