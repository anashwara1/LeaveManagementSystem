from django.db import models

# Create your models here.
from Users.models import Employees


class Leavebalance(models.Model):
    balance_id = models.AutoField(db_column='Balance_ID', primary_key=True)  # Field name made lowercase.
    empid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='Emp_ID', blank=True, null=True)  # Field name made lowercase.
    leave_earned = models.FloatField(db_column='Leave_Earned', blank=True, null=True)
    leave_consumed = models.FloatField(db_column='Leave_Consumed', blank=True, null=True)
    carry_forward = models.FloatField(db_column='Carry_Forward', blank=True, null=True)
    LOP = models.FloatField(db_column='LOP', blank=True, null=True)
    comp_off = models.FloatField(db_column='Comp_Off', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'LeaveBalance'


class LeaveRequest(models.Model):
    leave_request_id = models.AutoField(db_column='Leave_Request_ID', primary_key=True)  # Field name made lowercase.
    emp = models.ForeignKey(Employees, models.DO_NOTHING, db_column='Emp_ID', blank=True, null=True)  # Field name made lowercase.
    leavetypeid = models.ForeignKey('LeaveTypes', models.DO_NOTHING, db_column='LeaveTypeID', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=300, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Leave_Request'


class LeaveTypes(models.Model):
    leave_type_id = models.AutoField(db_column='Leave_Type_ID', primary_key=True)  # Field name made lowercase.
    leave_type_name = models.CharField(db_column='Leave_Type_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Leave_Types'


class Holidays(models.Model):
    holiday_id = models.AutoField(db_column='Holiday_ID', primary_key=True)
    holiday_name = models.CharField(db_column='Holiday', max_length=100, blank=True, null=True)
    date = models.DateField(db_column='Date', blank=True, null=True)
    day = models.CharField(db_column='Day', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Holidays'
