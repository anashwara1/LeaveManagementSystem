from django.db import models

# Create your models here.
from Users.models import Employees


class Leavebalance(models.Model):
    balance_id = models.AutoField(db_column='Balance_ID', primary_key=True)  # Field name made lowercase.
    empid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='Emp_ID', blank=True, null=True)  # Field name made lowercase.
    leavetypeid = models.ForeignKey('LeaveTypes', models.DO_NOTHING, db_column='LeaveTypeID', blank=True, null=True)  # Field name made lowercase.
    balance = models.IntegerField(db_column='Balance', blank=True, null=True)  # Field name made lowercase.

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
    max_leave_days = models.IntegerField(db_column='Max_Leave_Days', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Leave_Types'

