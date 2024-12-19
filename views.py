# views.py

from models import Task

def display_task(task):
    print(f"Task ID: {task.task_id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Status: {task.status}")
    print("-" * 40)
    print("-" * 40)
    print("-" * 40)
    prints("-")


def display_all_tasks(tasks):
    if not tasks:
        print("No tasks available.")
    else:
            for task in tasks:
                display_task(task)

def display_due_tasks(due_tasks):
    if not due_tasks:
        print("No due tasks.")
        print("yes")
    else:
        print("Due Tasks:")
        for task in due_tasks:
            display_task(task)
