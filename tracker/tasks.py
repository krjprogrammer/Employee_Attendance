from datetime import datetime, timedelta
import time
import sqlite3
import calendar


connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

def calculate_attendance_with_leaves(month, year):
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    attendance_query = """
        SELECT employee_id, COUNT(*) as attendance_count
        FROM tracker_mark_attendance_report
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        GROUP BY employee_id
    """
    cursor.execute(attendance_query, (f"{month:02d}", str(year)))
    attendance_counts = cursor.fetchall()
    leave_query = """
        SELECT employee_id, from_date, to_date
        FROM tracker_employee_leave_table
        WHERE grant = 1
    """
    cursor.execute(leave_query)
    leave_records = cursor.fetchall()

    leave_days_dict = {}
    for employee_id, from_date, to_date in leave_records:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
        adjusted_from_date = max(from_date, first_day_of_month)
        adjusted_to_date = min(to_date, last_day_of_month)
        
        if adjusted_from_date <= adjusted_to_date:
            leave_days = (adjusted_to_date - adjusted_from_date).days + 1
            if employee_id in leave_days_dict:
                leave_days_dict[employee_id] += leave_days
            else:
                leave_days_dict[employee_id] = leave_days

    attendance_with_leaves = []
    for employee_id, attendance_count in attendance_counts:
        leave_days = leave_days_dict.get(employee_id, 0)
        net_attendance = attendance_count - leave_days
        attendance_with_leaves.append({
            "employee_id": employee_id,
            "attendance_count": net_attendance
        })

    return attendance_with_leaves

result = calculate_attendance_with_leaves(month=8, year=2024)
connection.close()


def get_employee_payroll(employee_id):
    try:
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute("SELECT payroll FROM tracker_employee_details WHERE employee_id = ?", (employee_id,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return 1000  

    except Exception as e:
        print(f"Error: {e}")
        return 1000
    finally:
        if connection:
            connection.close()


def insert_salary_data(emp_id, emp_name, month, salary, status,year):
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO tracker_employee_salary_model (Emp_id, Emp_name, Month, Year, Salary, Status)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (emp_id, emp_name, month, year, salary, status))
    connection.commit()
    connection.close()

def check_first_day_of_month():
    while True:
        today = datetime.now()
        if today.day == 1:
            previous_month = (today - timedelta(days=1)).month
            previous_month_name = calendar.month_name[previous_month]
            current_year = today.year
            attendance_list = calculate_attendance_with_leaves(previous_month,current_year)
            for i in attendance_list:
                emp_id = i["employee_id"]
                connection = sqlite3.connect("db.sqlite3")
                cursor = connection.cursor()
                cursor.execute("SELECT employee_first_name FROM tracker_employee_details WHERE employee_id = ?", (emp_id,))
                name = cursor.fetchone()
                pay = get_employee_payroll(emp_id)
                att_count = i["attendance_count"]
                salary =  pay*att_count
                status  = "pending"
                insert_salary_data(emp_id,name,previous_month_name,salary,status,current_year)

            
        else:
            print("Today is not the first day of the month.")

        time.sleep(24 * 60 * 60)


check_first_day_of_month()

