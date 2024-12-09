# utilities.py

def format_task_details(task):
    return (
        f"Task ID: {task.task_id}\n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n"
        f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Status: {task.status}\n"
    )
