from django.urls import path
from .views import LeaveListView, Employee_Login,AttendanceReportView,Check_location,Employee_Registration,User_Login,Upload_employee_details,Mark_attendance,Declare_Geofenced_area,get_user_data,upload_images,recognize_user,LeaveView
from .views import GrantLeaveView,Payroll_View,update_payment_status,fetch_month_wise_payroll,CalculateManualPayroll,count_unique_employee_ids,count_unique_employee_ids_today
from .views import AddEmployeeData,bank_details,RemoveEmployee,UpdateEmployeeData,UpdateUserDetailsView,EmployeeAttendanceList,LeaveStatus,SendEmployeeDataOnly,UploadProfilePhotoView,att_dumy

urlpatterns = [
    path('register',Employee_Registration.as_view()),
    path('login',User_Login.as_view()),
    path('employee_login',Employee_Login.as_view()),
    path('upload_employee_data',Upload_employee_details),
    path('mark_attendance',Mark_attendance),
    path('Declare_area',Declare_Geofenced_area.as_view()),
    path('get_user_data',get_user_data.as_view()),
    path('check_location',Check_location.as_view()),
    path('get_attendance_report/', AttendanceReportView.as_view(), name='get_attendance_report'),
    path('upload_images/',upload_images),
    path('recognize_employee',recognize_user),
    path('employee_login',Employee_Login.as_view()),
    path('apply_for_leave',LeaveView.as_view()),
    path('leave_list/', LeaveListView.as_view(), name='leave_list'),
    path('grant_leave',GrantLeaveView.as_view()),
    path('salary_data',Payroll_View.as_view()),
    path('salary_data/<int:year>/<str:month>/', fetch_month_wise_payroll, name='fetch_month_wise_payroll'),
    path('update_status',update_payment_status.as_view()),
    path('cal_manual_salary',CalculateManualPayroll.as_view()),
    path('get_employees_count',count_unique_employee_ids),
    path('get_employees_count_today',count_unique_employee_ids_today),
    path('get_bank_details',bank_details),
    path('remove_employees',RemoveEmployee.as_view()),
    path('update_employee',UpdateEmployeeData.as_view()),
    path('update_profile',UpdateUserDetailsView.as_view()),
    path('emp_attendance',EmployeeAttendanceList.as_view()),
    path('leave_status',LeaveStatus.as_view()),
    path('employee_data_only',SendEmployeeDataOnly.as_view()),
    path('upload-profile-photo/', UploadProfilePhotoView.as_view(), name='upload-profile-photo'),
    path('up',att_dumy),
    path('add_employee',AddEmployeeData.as_view()),
    # path('temp_salary',insert_dumy_salary_data)
]