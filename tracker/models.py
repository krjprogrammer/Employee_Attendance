from django.db import models
from django.utils import timezone

class user_data(models.Model):
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    username = models.CharField(max_length=255,null=True, blank=True)
    email_id = models.CharField(max_length=255,null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    confirm_password = models.CharField(max_length=255,null=True, blank=True)
    mobile_number = models.CharField(max_length=255,null=True, blank=True)


class employee_register_table(models.Model):
    employee_username = models.CharField(max_length=255,null=True, blank=True)
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    employee_id = models.CharField(max_length=255,null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    mobile_number = models.CharField(max_length=255,null=True, blank=True)
    employee_email_id = models.CharField(max_length=255,null=True, blank=True)
    confirm_password = models.CharField(max_length=255,null=True, blank=True)


class employee_details(models.Model):
    employee_id = models.CharField(max_length=255,null=True, blank=True)
    employee_first_name = models.CharField(max_length=255,null=True, blank=True)
    employee_last_name = models.CharField(max_length=255,null=True, blank=True)
    employee_email_id = models.CharField(max_length=255,null=True, blank=True)
    employee_mobile_number = models.CharField(max_length=255,null=True, blank=True)
    employee_image_encodeing = models.BinaryField(null=True)
    profile_photo =  models.TextField(null=True, blank=True) 
    employee_account_number = models.CharField(max_length=255,null=True, blank=True)
    employee_bank = models.CharField(max_length=255,null=True, blank=True)
    employee_bank_ifsc_code = models.CharField(max_length=255,null=True, blank=True)
    payroll = models.CharField(max_length=255,null=True, blank=True)

class mark_attendance_report(models.Model):
    employee_id = models.CharField(max_length=255, null=True, blank=True)
    employee_name = models.CharField(max_length=255, null=True, blank=True)
    employee_photo = models.BinaryField(null=True)
    date = models.CharField(max_length=10, editable=False) 
    time = models.TimeField(default=timezone.now)  # Keep time as TimeField
    mark = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.date = timezone.now().strftime('%Y-%m-%d') 
        super().save(*args, **kwargs)

class GeofencedArea(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.FloatField(help_text="Radius in meters")

class employee_leave_data(models.Model):
    Emp_id = models.CharField(max_length=100)
    Emp_name = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    reason = models.TextField()
    grant = models.BooleanField(default=False,null=True)

class employee_salary_model(models.Model):
    Emp_id = models.CharField(max_length=100)
    Emp_name = models.CharField(max_length=100)
    Month = models.CharField(max_length=100)
    Year = models.CharField(max_length=100)
    Salary = models.IntegerField()
    Status = models.CharField(max_length = 100)


