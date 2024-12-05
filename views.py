# views.py

from models import Task

def display_task(task):
    print(f"Task ID: {task.task_id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Status: {task.status}")
    print("-" * 40)

def display_all_tasks(tasks):
    for task in tasks:
        display_task(task)
