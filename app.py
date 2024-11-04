from flask import Flask, render_template, request, redirect
from datetime import datetime, date, timedelta
import random


app = Flask(__name__)

# เก็บรายการ To-Do
todos = []



@app.route('/')
def index():
    
    # คำนวณเปอร์เซ็นต์การเสร็จสิ้น
    completion_percentage = calculate_completion_percentage()
    # จัดเรียงรายการตามสถานะการเสร็จสิ้น
    sorted_todos = sorted(todos, key=lambda x: x['completed'], reverse=True)
    main_task = random.choice(todos) if todos else None  # สุ่มงานประจำวัน
    return render_template("index.html", todos=sorted_todos, completion_percentage=completion_percentage, main_task=main_task)

@app.route('/add', methods=['POST'])  # เพิ่มรายการ
def add_todo():
    todo = request.form.get('todo')
    priority = request.form.get('priority') or ''  # รับค่าความสำคัญ
    due_date = request.form.get('due_date')  # รับค่าวันกำหนดเส้นตาย
    if todo :
        if due_date:  
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
        else:
            due_date_obj = None  
        todos.append({'task': todo, 'completed': False, 'priority': priority, 'due_date': due_date_obj})
    return redirect('/')

@app.route('/complete/<int:todo_id>', methods=['POST'])  # เปลี่ยนสถานะรายการ
def complete_todo(todo_id):
    if 0 <= todo_id < len(todos):
        todos[todo_id]['completed'] = not todos[todo_id]['completed']
    return redirect('/')

@app.route('/uncomplete/<int:todo_id>', methods=['POST'])  # ยกเลิกสถานะการทำเสร็จของรายการ
def uncomplete_todo(todo_id):
    if 0 <= todo_id < len(todos):
        todos[todo_id]['completed'] = False
    return redirect('/')

@app.route('/delete/<int:todo_id>')  # ลบรายการ
def delete_todo(todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return redirect('/')

@app.route('/alltask')
def alltask():
    return render_template('alltask.html')

@app.route('/myday')
def myday():
    today = date.today()  # วันปัจจุบัน
    # กรองรายการที่มีเดดไลน์เป็นวันนี้
    today_todos = [todo for todo in todos if todo['due_date'] and todo['due_date'].date() == today]
    
    return render_template("myday.html", todos=today_todos)

@app.route('/monthly')
def monthly():
    today = date.today()
    # กำหนดเดือนและปีปัจจุบัน
    current_month = today.month
    current_year = today.year
    
    # กรองรายการที่อยู่ในเดือนและปีปัจจุบัน
    monthly_todos = [todo for todo in todos if todo['due_date'] and todo['due_date'].month == current_month and todo['due_date'].year == current_year]
    
    return render_template('monthly.html', todos=monthly_todos)

def calculate_completion_percentage():  # คำนวณเปอร์เซ็นต์
    if not todos:
        return 0
    completed_count = sum(1 for todo in todos if todo['completed'])
    return (completed_count / len(todos)) * 100

@app.route('/weekly_tasks')
def weekly_tasks():
    start_of_week = date.today() - timedelta(days=date.today().weekday())  # วันจันทร์ของสัปดาห์นี้
    end_of_week = start_of_week + timedelta(days=6)  # วันอาทิตย์ของสัปดาห์นี้

    # กรองรายการที่อยู่ในช่วงวันที่ของสัปดาห์นี้
    weekly_todos = [todo for todo in todos if todo['due_date'] and start_of_week <= todo['due_date'].date() <= end_of_week]
    
    return render_template("weekly_tasks.html", todos=weekly_todos)


if __name__ == '__main__':
    app.run(debug=True)
