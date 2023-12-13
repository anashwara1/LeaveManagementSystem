from django.db import models

# Create your models here.
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
        department_name = input("Department: ")
        designation_name = input("Designation: ")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('balance', 2)

        department, created = Department.objects.get_or_create(dep_name=department_name)
        designation, created = Designation.objects.get_or_create(designation=designation_name, dep=department)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff true')

        user = self.create_user(email, password, **extra_fields)

        user.department = department
        user.designation = designation
        user.save()

        manager = Managers(emp=user)
        manager.save()

        return user



class Employees(AbstractUser, PermissionsMixin):
    username = None
    emp_id = models.CharField(db_column='Emp_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='email', max_length=100, unique=True, default='anu@mail.com')  # Field name made lowercase.
    password = models.CharField(max_length=128, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, db_column='Department_id', blank=True, null=True)  # Field name made lowercase.
    designation = models.ForeignKey(Designation, models.DO_NOTHING, db_column='desig_id', blank=True, null=True)
    date_of_joining = models.DateField(db_column='Date_of_Joining', blank=True, null=True)  # Field name made lowercase.
    managed_by = models.ForeignKey('Managers', models.DO_NOTHING, db_column='Managed_by', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(default=True)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='Updated_at', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase.
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    balance = models.IntegerField(db_column='Balance', blank=True, null=True)  # Field name made lowercase.
    is_manager = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['emp_id', 'firstname', 'lastname', 'date_of_joining']

    def natural_key(self):
        return (self.email,)

    class Meta:
        managed = True
        db_table = 'Employees'


class Managers(models.Model):
    manager_id = models.AutoField(db_column='Manager_ID', primary_key=True)  # Field name made lowercase.
    emp = models.ForeignKey(Employees, models.DO_NOTHING, db_column='EMP_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Managers'
