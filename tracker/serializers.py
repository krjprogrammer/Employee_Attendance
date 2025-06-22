from rest_framework import serializers
from .models import user_data,employee_details,employee_leave_data,employee_salary_model,mark_attendance_report
class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_data
        fields = '__all__'

class employee_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = employee_details
        fields = '__all__'

class EmployeeLeaveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_leave_data
        fields = '__all__'

class Payroll_Serialzer(serializers.ModelSerializer):
    class Meta:
        model = employee_salary_model
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = mark_attendance_report
        fields = '__all__'