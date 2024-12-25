# services.py

from models import Task
from datetime import datetime, timedelta
from utilities import format_task_details

class TaskService:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date, status="Pending"):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, description, due_date, status)
        self.tasks.append(task)
        

    def get_due_tasks(self):
        return [task for task in self.tasks if task.is_due()]

    def mark_task_as_complete(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            task.mark_complete()

    def get_formatted_task_details(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            return format_task_details(task)
        return "Task not found"

print(my_var)
