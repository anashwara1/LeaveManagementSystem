# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class Department(models.Model):
    department_id = models.AutoField(db_column='Department_ID', primary_key=True)  # Field name made lowercase.
    dep_name = models.CharField(db_column='Dep_Name', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Department'


class Designation(models.Model):
    designation_id = models.AutoField(db_column='Designation_ID', primary_key=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dep = models.ForeignKey(Department, models.DO_NOTHING, db_column='Dep_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Designation'

class CustomUserManager(BaseUserManager):

    use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff true')

        return self.create_user(email, password, **extra_fields)


class Employees(AbstractUser, PermissionsMixin):
    username = None
    emp_id = models.CharField(db_column='Emp_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='email', max_length=100, unique=True, default='anu@mail.com')  # Field name made lowercase.
    password = models.CharField(max_length=128, null=True, blank=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, db_column='Department_id', blank=True, null=True)  # Field name made lowercase.
    date_of_joining = models.DateField(db_column='Date_of_Joining', blank=True, null=True)  # Field name made lowercase.
    managed_by = models.ForeignKey('Managers', models.DO_NOTHING, db_column='Managed_by', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(default=True)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='Updated_at', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase.
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def natural_key(self):
        return (self.email,)
    class Meta:
        managed = True
        db_table = 'Employees'


class Leavebalance(models.Model):
    balance_id = models.AutoField(db_column='Balance_ID', primary_key=True)  # Field name made lowercase.
    empid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='EmpID', blank=True, null=True)  # Field name made lowercase.
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


class Managers(models.Model):
    manager_id = models.AutoField(db_column='Manager_ID', primary_key=True)  # Field name made lowercase.
    emp = models.ForeignKey(Employees, models.DO_NOTHING, db_column='EMP_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Managers'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_user'
#
#
# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'views_auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'views_django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = True
#         db_table = 'views_django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'views_django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'views_django_session'
