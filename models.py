# models.py

from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, due_date, status):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    def is_due(self):
        return datetime.now() > self.due_date

    def mark_complete(self):
        self.status = "Completed"
