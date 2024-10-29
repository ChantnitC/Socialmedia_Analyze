from flask import Flask, render_template, request, redirect
from datetime import datetime, date
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

def calculate_completion_percentage():  # คำนวณเปอร์เซ็นต์
    if not todos:
        return 0
    completed_count = sum(1 for todo in todos if todo['completed'])
    return (completed_count / len(todos)) * 100

if __name__ == '__main__':
    app.run(debug=True)
