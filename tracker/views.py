from django.shortcuts import render
import face_recognition
from datetime import date
import numpy as np
from datetime import datetime,timedelta
from datetime import datetime
import calendar
from django.shortcuts import get_list_or_404
from django.conf import settings
import jwt
from django.http import JsonResponse
from .models import user_data,employee_register_table,employee_leave_data
from .serializers import user_serializer,employee_data_serializer,EmployeeLeaveDataSerializer,Payroll_Serialzer,AttendanceSerializer
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from django.utils.timezone import now
from sqlalchemy import create_engine
from rest_framework.decorators import api_view
import base64
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from io import BytesIO
import hashlib
from .models import employee_details,mark_attendance_report,GeofencedArea,user_data,employee_leave_data,employee_salary_model
# import face_recognition
import math
from email.mime.text import MIMEText
import openpyxl
from openpyxl import Workbook
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication
import smtplib
# Create your views here.

college_coordinates = {
    "lat":20.781563, "long":76.677696
}

home_coordinates = {
    "lat":20.75986299098946,"long":78.62035945817749
}

second_home_coordinates = {
    "lat":20.7599075,"long":78.6195375
}

Comapny_details = {
    'name':'Pharmagretech.LTD',
    'latitude':college_coordinates['lat'],
    'longitude':college_coordinates['long'],
    'radius':1200
}

smtp_config = {
    'host': 'mail.privateemail.com',
    'port': 465,
    'user': 'support@disruptionsim.com',
    'password': 'Onesmarter@2023'
}

def send_fire_email(email,removal_date,balance,reason,emp_name):
    server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
    server.login(smtp_config['user'], smtp_config['password'])
    balance = float(balance)
    if balance > 0:
        paycheck_info = f"Your final paycheck, including a balance salary of ${balance}, will be processed and provided to you by {removal_date}."
    else:
        paycheck_info = ""

    msg = MIMEMultipart()
    msg['From'] = smtp_config['user']
    msg['To'] = email
    msg['Subject'] = f"Important: Update Regarding Your Employment Status"

    body = f"""
    Dear {emp_name},

    I hope this message finds you well.

    After careful consideration, we regret to inform you that we have made the difficult decision to terminate your employment with [Company Name], effective {removal_date}.

    This decision was made due to {reason}. We truly appreciate the contributions you have made during your time with us, and we acknowledge your efforts and dedication to your role.

    {paycheck_info}. Additionally, you will receive details about your severance package, benefits continuation, and other relevant information.

    Should you have any questions or need further assistance, please do not hesitate to reach out to HR. We are here to support you during this transition.

    We wish you all the best in your future endeavors.

    Sincerely,   
    [Pharmagretech]  
    """
    msg.attach(MIMEText(body, 'html'))

    server.send_message(msg, from_addr=smtp_config['user'], to_addrs=email)
    server.quit()
    print(f"termination email sent successfully")

def send_resignation_email(email,removal_date,balance,reason,emp_name):
    server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
    server.login(smtp_config['user'], smtp_config['password'])
    balance = float(balance)
    if balance > 0:
        paycheck_info = f"Your final paycheck, including a balance salary of ${balance}, will be processed and provided to you by {removal_date}."
    else:
        paycheck_info = ""

    msg = MIMEMultipart()
    msg['From'] = smtp_config['user']
    msg['To'] = email
    msg['Subject'] = f"Important: Update Regarding Your Employment Status"

    body = f"""
        Dear {emp_name},

        I hope this message finds you well.

        We have received and acknowledged your resignation from your position at [Company Name], effective {removal_date}. While we are saddened to see you leave, we respect your decision and wish you success in your future endeavors.

        Your contributions during your time with us have been truly appreciated, and your efforts have not gone unnoticed. We value the positive impact you’ve made on the team and the organization.

        {paycheck_info}

        Additionally, we will share details about the handover process, benefits continuation, and any other pertinent information shortly.

        If you have any questions or require assistance during this transition, please don’t hesitate to contact [HR Contact Person] at [HR Contact Email] or [HR Contact Phone Number].

        Thank you once again for your hard work and dedication. We wish you all the very best in your next chapter.

        Sincerely,  
        [Your Full Name]  
        [Your Job Title]  
        [Company Name]  
        [Company Contact Information]
        """
    msg.attach(MIMEText(body, 'html'))
    server.send_message(msg, from_addr=smtp_config['user'], to_addrs=email)
    server.quit()
    print(f"termination email sent successfully")


class Employee_Registration(APIView):
    def hash_password(self,password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    def post(self,request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_name = data.get('username')
        if employee_register_table.objects.filter(employee_username=user_name).exists():
            return Response('Username not available, try another')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password == confirm_password:
            pass_hash = self.hash_password(password)
            confirm_hash = pass_hash
            mobile_number = data.get('mobile_number')
            email_id = data.get('email')
            emp_id = data.get('employee_id')
            instance = employee_register_table.objects.create(first_name=first_name,last_name=last_name,employee_username=user_name,employee_email_id=email_id,password=pass_hash,confirm_password=confirm_hash,mobile_number=mobile_number,employee_id=emp_id)
            return Response('employee registered sucessfully')
        else:
            return Response('password doesnot match please try again')

class get_user_data(APIView):
    def get(self,request):
        db_data = user_data.objects.all()
        serializer = user_serializer(db_data,many=True)
        return Response(serializer.data)


class Employee_Login(APIView):
    SECRET_KEY = settings.SECRET_KEY
    def hash_password(self,password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print("hashed_password",hashed_password)
        return hashed_password
    
    def generate_token(self, username: str) -> str:
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
        return token
    
    def post(self,request):
        data = request.data
        username = data.get('username')
        print(username)
        password = data.get('password')
        try:
            username_check = employee_register_table.objects.get(employee_id=username)
            if username_check:
                try:
                    hash_pass = self.hash_password(password)
                    password_check = employee_register_table.objects.get(employee_id=username,password=hash_pass)
                    if password_check:
                        token = self.generate_token(username)
                        return Response({"message":'employee logged in sucessfully','token':token})
                    else:
                        return Response('password is incorrect')
                except:
                    return Response('Password is incorrect')
            else:
                return Response('Username does not match')
        except:
            return Response('Username does not match')


class User_Login(APIView):
    SECRET_KEY = settings.SECRET_KEY

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self, username: str) -> str:
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
        return token

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            username_check = user_data.objects.get(username=username)
            if username_check:
                hash_pass = self.hash_password(password)
                if username_check.password == hash_pass:
                    token = self.generate_token(username)
                    return Response({'message': 'User logged in successfully', 'token': token})
                else:
                    return Response({'error': 'Password is incorrect'}, status=401)
            else:
                return Response({'error': 'Username does not match'}, status=404)
        except user_data.DoesNotExist:
            return Response({'error': 'Username does not match'}, status=404)
        

@api_view(['POST'])
def Upload_employee_details(request):
    uploaded_file = request.FILES.get('file')
    try:
        df_csv = pd.read_excel(BytesIO(uploaded_file.read()))
        print(df_csv)
        df_csv.columns = df_csv.columns.str.strip()
        df_csv.columns = df_csv.columns.str.strip().str.replace('-', '').str.replace(r'\s+', ' ', regex=True).str.replace(' ', '_')
        DATABASE_URI = 'sqlite:///db.sqlite3'

        engine = create_engine(DATABASE_URI)

        table_name = 'tracker_employee_details'
        df_csv.to_sql(table_name, con=engine, if_exists='append', index=False)

        engine.dispose()
        return Response('Employess Logged Sucessfully')
    except Exception as e:
        return Response({'error': str(e)}, status=400)



class Check_location(APIView):
    def haversine_distance(self,lat1, lon1, lat2, lon2):
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
    
    def set_company_geolocation(self):
        instance = GeofencedArea(name=Comapny_details['name'],latitude=Comapny_details['latitude'],longitude=Comapny_details['longitude'],radius=Comapny_details['radius'])
        instance.save()

    def post(self,request):
        self.set_company_geolocation()
        data = request.data
        user_lat = float(data.get('lat'))
        user_lon = float(data.get('long'))
        geofenced_area = GeofencedArea.objects.last()
        print(geofenced_area)
        print(geofenced_area.radius)
        distance = self.haversine_distance(user_lat, user_lon, geofenced_area.latitude, geofenced_area.longitude)
        print(distance)
        if distance <= geofenced_area.radius:
            return Response('Employee in the office area')
        else:
            return Response('Sorry but you are out of the office area')

@api_view(['POST'])             
def Mark_attendance(request):
        employee_name = request.POST.get('employee_name')
        employee_id = request.POST.get('employee_id')
        print(employee_id)
        mark = request.POST.get('mark')
        uploaded_image = request.FILES.get('image')
        msg = recognize_user(uploaded_image)
        msg = msg.strip()
        employee_name = employee_name.strip()
        if msg == "No image file provided.":
            return Response(msg)
        elif msg == "Error in processing image":
            return Response(msg)
        elif msg == "No face detected in the uploaded image.":
            return Response(msg)
        elif msg ==  "No match found.":
            return Response(msg)
        elif msg == employee_name:
            employee_exists = employee_details.objects.get(employee_first_name=employee_name,employee_id=employee_id)
            try:
                if employee_exists:
                    if mark:
                            current_date = date.today().strftime("%Y-%m-%d")
                            if mark_attendance_report.objects.filter(date=current_date,employee_id=employee_id).exists():
                                return Response("Attendance already marked")
                            else:
                                instance = mark_attendance_report(employee_id=employee_id,employee_name = employee_name,mark='Present')
                                instance.save()
                                return Response(f'Attendance Marked Sucessfully')
                    else:
                            return Response('please mark the attandance')
            except Exception as e:
                    return Response('Employee data not available please try again')
        else:
            print("blah blah")
            return Response("No match found.")
        
class Declare_Geofenced_area(APIView):
    def post(self,request):
        data = request.data
        company_name = data.get('company_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius')
        instance = GeofencedArea(name=company_name,latitude=latitude,longitude=longitude,radius=radius)
        instance.save()
        return Response('Area Marked Sucessfully')

@api_view(['POST'])
def upload_images(request):
    images = request.FILES.getlist('images')
    def encode_face(image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]
        else:
            raise ValueError("No face found in the image.")
    for image in images:
        filename = image.name
        name_without_extension = filename.rsplit('.', 1)[0]
        if name_without_extension.startswith("EMP_"):
            print(name_without_extension)
            employee_id = name_without_extension[4:]
            face_recognition_encoding = encode_face(image)
            print(employee_id)
            face_instance = employee_details.objects.get(employee_id=employee_id)
            image.seek(0)
            image_data = image.read()
            base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
            if face_instance:
                face_instance.employee_image_encodeing = face_recognition_encoding.tobytes()
                face_instance.profile_photo = base64_encoded_image
                print(base64_encoded_image)
                face_instance.save()
            else:
                return Response(f"Employee with employee id {employee_id} does not exists")
        else:
            employee_id = None
            print(f"Processing image for employee ID: {employee_id}")
            pass

    return Response("Images uploaded successfully")

def recognize_user(uploaded_image):
    if not uploaded_image:
        return "No image file provided."
    
    try:
        image = face_recognition.load_image_file(uploaded_image)
        encodings = face_recognition.face_encodings(image)
    except Exception as e:
        return f"Error in processing image"

    if not encodings:
        return "No face detected in the uploaded image."
    
    uploaded_encoding = encodings[0]
    users = employee_details.objects.all()

    for user in users:
        if user.employee_image_encodeing:
            stored_encoding = np.frombuffer(user.employee_image_encodeing, dtype=np.float64)
            match = face_recognition.compare_faces([stored_encoding], uploaded_encoding, tolerance=0.6)
            if match[0]:
                return f"{user.employee_first_name}"

    return "No match found."

class AttendanceReportView(APIView):
    def get(self, request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=10)
        attendance_records = mark_attendance_report.objects.filter(date__range=[start_date, end_date]).values(
            'id', 'employee_id', 'date', 'time', 'employee_name', 'mark'
        )
        
        attendance_list = [
            {
                **record,
                'time': record['time'].strftime("%H:%M") if record['time'] else None
            }
            for record in attendance_records
        ]

        return Response(attendance_list, status=status.HTTP_200_OK)
    
class LeaveView(APIView):
    def post(self, request):
        data = request.data
        emp_id = data.get("emp_id")
        emp_name = data.get("emp_name")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        reason = data.get("reason")
        existing_leave = employee_leave_data.objects.filter(
            Emp_id=emp_id, from_date=from_date, to_date=to_date
        ).exists()

        if existing_leave:
            return Response(
                {"message": "Leave application for the entered dates already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_data = employee_leave_data(
            Emp_id=emp_id,
            Emp_name=emp_name,
            from_date=from_date,
            to_date=to_date,
            reason=reason
        )
        
        leave_data.save()

        return Response({"message": "Leave data saved successfully."}, status=status.HTTP_201_CREATED)

    
class LeaveListView(APIView):
    def get(self, request):
        leave_data = employee_leave_data.objects.all()
        serializer = EmployeeLeaveDataSerializer(leave_data, many=True)
        return Response(serializer.data)

class GrantLeaveView(APIView):
    def post(self, request):
        data = request.data
        emp_id = data.get("Emp_id")
        grants = data.get("grant")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        try:
            leave_data = employee_leave_data.objects.get(Emp_id=emp_id, from_date=from_date, to_date=to_date)
            leave_data.grant = grants
            leave_data.save()

            return Response({"message": "Leave grant updated successfully."}, status=status.HTTP_200_OK)
        
        except employee_leave_data.DoesNotExist:
            return Response({"message": "Leave entry not found for the specified employee and date range."}, status=status.HTTP_404_NOT_FOUND)
        
# class Payroll_View(APIView):
#     def get(self,request):
#         today = datetime.now()
#         previous_month = (today - timedelta(days=1)).month
#         print(previous_month)
#         current_year = today.year
#         print(current_year)
#         previous_month_name = calendar.month_name[previous_month]
#         print(previous_month_name)
#         salary_data = employee_salary_model.objects.filter(Month=previous_month_name,Year=current_year)
#         serializer = Payroll_Serialzer(salary_data,many=True)
#         return Response(serializer.data)


class Payroll_View(APIView):
    def get(self, request):
        today = datetime.now()
        if today.month == 1:
            previous_month = 12
            current_year = today.year - 1
        else:
            previous_month = today.month - 1
            current_year = today.year

        previous_month_name = calendar.month_name[previous_month]
        salary_data = employee_salary_model.objects.filter(Month=previous_month_name, Year=current_year)
        serializer = Payroll_Serialzer(salary_data, many=True)

        return Response(serializer.data)

def fetch_month_wise_payroll(request, year, month):
    try:
        payrolls = get_list_or_404(employee_salary_model, Year=year, Month=month)
        payroll_data = [
            {
                'Emp_id': payroll.Emp_id,
                'Emp_name': payroll.Emp_name,
                'Month': payroll.Month,
                'Year': payroll.Year,
                'Salary': payroll.Salary,
                'status': payroll.Status
            } for payroll in payrolls
        ]
        return JsonResponse(payroll_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class update_payment_status(APIView):
    def post(self,request):
        emp_id = request.data.get('emp_id')
        instance = employee_salary_model.objects.get(Emp_id = emp_id)
        instance.Status = "Paid"
        instance.save()
        return Response("Marked as paid")

class CalculateManualPayroll(APIView):
    def post(self,request):
        emp_name = request.data.get("emp_name")
        emp_id = request.data.get("emp_id")
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        employee = employee_details.objects.get(employee_first_name=emp_name,employee_id=emp_id)
        payroll = employee.payroll
        from_date = from_date.split("T")[0]  # Get only 'YYYY-MM-DD' part
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = to_date.split("T")[0]  # Get only 'YYYY-MM-DD' part
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        date_difference = to_date - from_date
        total_days = date_difference.days
        payroll = int(payroll)
        if payroll != None:
            salary = payroll*total_days
        else:
            salary = 1000*total_days
        if salary < 0:
            return Response("Invalid Date Selected")
        else:
            return Response(f"Salary for the selected time period =  ₹ {salary}")
    
def count_unique_employee_ids(request):
    unique_employee_count = employee_details.objects.values('employee_id').distinct().count()
    print(unique_employee_count)
    return JsonResponse({'unique_employee_count': unique_employee_count})

def count_unique_employee_ids_today(request):
    today_date = now().date()
    unique_employee_count_today = mark_attendance_report.objects.filter(date=today_date).values('employee_id').distinct().count()
    print(unique_employee_count_today)
    return JsonResponse({'unique_employee_count_today': unique_employee_count_today})

def bank_details(request):
    employees = employee_details.objects.values(
        'employee_id',
        'employee_first_name',
        'employee_email_id',
        'employee_mobile_number',
        'employee_bank',
        'employee_account_number',
        'employee_bank_ifsc_code'
    ).distinct()
    bank_details_list = list(employees)
    return JsonResponse({'bank_details': bank_details_list})


class RemoveEmployee(APIView):
    def post(self,request):
        emp_id  = request.data.get('employee_id')
        removal_date = request.data.get('date_of_removal')
        emp_name = request.data.get('emp_name')
        reason = request.data.get('reason')
        balance = request.data.get('balance_salary')
        termination_type = request.data.get('termination_type')
        instance = employee_details.objects.get(employee_id=emp_id)
        email = instance.employee_email_id
        if termination_type == "Fire":
            send_fire_email(email,removal_date,balance,reason,emp_name)
        else:
            send_resignation_email(email,removal_date,balance,reason,emp_name)
        instance.delete()
        instance.save()
        return Response('Employee Removed Sucessfully')

class UpdateEmployeeData(APIView):
        def post(self,request):
            employee_id = request.data.get('employee_id')
            employee_first_name = request.data.get('employee_first_name')
            employee_last_name = request.data.get('employee_last_name')
            employee_email_id = request.data.get('employee_email_id')
            mobile_number = request.data.get('mobile_number')
            employee_account_number = request.data.get('employee_account_number')
            employee_bank = request.data.get('employee_bank')
            employee_bank_ifsc_code = request.data.get('employee_bank_ifsc_code')
            payroll = request.data.get('payroll')
            instance = employee_details.objects.get(employee_id=employee_id)
            fields = {
                "employee_first_name": employee_first_name,
                "employee_last_name": employee_last_name,
                "employee_email_id": employee_email_id,
                "mobile_number": mobile_number,
                "employee_account_number": employee_account_number,
                "employee_bank": employee_bank,
                "employee_bank_ifsc_code": employee_bank_ifsc_code,
                "payroll": payroll,
            }
            non_empty_fields = {key: value for key, value in fields.items() if value}
            for key,value in non_empty_fields.items():
                 setattr(instance, key, value)
            instance.save()
            return Response('Employee Data Updated sucessfully')


class UpdateUserDetailsView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        user_name = request.data.get('use_name')
        last_name = request.data.get('last_name')
        email_id = request.data.get('email_id')
        password = request.data.get('password')
        mobile_number = request.data.get('mobile_number')
        try:
            user_instance = user_data.objects.get(username=user_name)
        except user_data.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        fields = {
            "first_name": first_name,
            "user_name": user_name,
            "last_name": last_name,
            "email_id": email_id,
            "password": password,
            "mobile_number": mobile_number,
        }

        non_empty_fields = {key: value for key, value in fields.items() if value}

        for key, value in non_empty_fields.items():
            setattr(user_instance, key, value)

        user_instance.save()

        return Response(
            {"message": "User details updated successfully", "updated_fields": non_empty_fields},
            status=status.HTTP_200_OK
        )
    
class EmployeeAttendanceList(APIView):
    def post(self,request):
        emp_id = request.data.get('emp_id')
        print("jinx",emp_id)
        db_data = mark_attendance_report.objects.filter(employee_id=emp_id).values()
        try:  
            return JsonResponse(list(db_data), safe=False)
        except Exception as e:
            return Response(f"ERROR: {e}")
        
class LeaveStatus(APIView):
    def post(self, request):
        emp_id = request.data.get("emp_id")
        print('rox',emp_id)
        db_data = employee_leave_data.objects.filter(Emp_id=emp_id)
        current_date = datetime.now().date()
        valid_data = db_data.filter(from_date__gte=current_date)
        serializer = EmployeeLeaveDataSerializer(valid_data, many=True)
        return Response(serializer.data)
    
class SendEmployeeDataOnly(APIView):
    def post(self,request):
        emp_id = request.data.get("EMP_ID")
        db_data = employee_details.objects.get(employee_id=emp_id)
        serializer = employee_data_serializer(db_data)
        return Response(serializer.data)

class UploadProfilePhotoView(APIView):
    def post(self, request):
        emp_id = request.data.get("emp_id")
        photo = request.FILES.get("photo")

        if not emp_id or not photo:
            return Response({"error": "Both emp_id and photo are required."}, status=400)

        try:
            photo_data = photo.read()
            base64_photo = base64.b64encode(photo_data).decode('utf-8')
            employee = employee_details.objects.get(employee_id=emp_id)
            employee.profile_photo = base64_photo
            employee.save()
            return Response({"message": "Profile photo uploaded successfully!"})
        except employee_details.DoesNotExist:
            return Response({"error": f"Employee with ID {emp_id} does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def att_dumy(request):
    uploaded_file = request.FILES.get('file')
    try:
        df_csv = pd.read_excel(BytesIO(uploaded_file.read()))
        df_csv.columns = df_csv.columns.str.strip()
        df_csv.columns = df_csv.columns.str.strip().str.replace('-', '').str.replace(r'\s+', ' ', regex=True).str.replace(' ', '_')
        DATABASE_URI = 'sqlite:///db.sqlite3'

        engine = create_engine(DATABASE_URI)

        table_name = 'tracker_mark_attendance_report'
        df_csv.to_sql(table_name, con=engine, if_exists='append', index=False)

        engine.dispose()
        return Response('attendance Logged Sucessfully')
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    

class AddEmployeeData(APIView):
    def post(self,request):
        required_fields = [
            "employee_id", "first_name", "last_name", "email_id",
            "mobile_number", "account_number", "bank_name", "bank_ifsc_code"
        ]

        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = employee_details.objects.create(
                    employee_id=request.data["employee_id"],
                    employee_first_name=request.data["first_name"],
                    employee_last_name=request.data["last_name"],
                    employee_email_id=request.data["email_id"],
                    employee_mobile_number=request.data["mobile_number"],
                    employee_account_number=request.data["account_number"],
                    employee_bank=request.data["bank_name"],
                    employee_bank_ifsc_code=request.data["bank_ifsc_code"],
                    payroll = request.data["payroll"]
                )
            return Response("Employee added sucessfully")
        except Exception as e:
            return Response(f"ERROR {e} ")
        

