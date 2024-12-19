# controllers.py

from services import TaskService
from views import display_all_tasks
from datetime import datetime, timedelta

def manage_tasks():
    task_service = TaskService()
    print(my_var)
    # Add tasks
    task_service.add_task("Finish homework", "Complete math homework", datetime.now() + timedelta(days=1))
    task_service.add_task("Grocery shopping", "Buy groceries", datetime.now() + timedelta(days=2))
    task_service.add_task("Clean the house", "Clean the entire house", datetime.now() + timedelta(days=3))

    # Display all tasks
    print("All Tasks:")
    display_all_tasks(task_service.tasks)

    # Mark the first task as complete
    task_service.mark_task_as_complete(1)

    # Display all tasks after marking one complete
    print("Updated Tasks:")
    display_all_tasks(task_service.tasks)
