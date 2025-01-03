# tests.py

import unittest
from models import Task
from services import TaskService
from datetime import datetime, timedelta

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_service = TaskService()

    def test_add_task(self):
        self.task_service.add_task("Test task", "Test description", datetime.now() + timedelta(days=1))
        self.assertEqual(len(self.task_service.tasks), 1)

    def test_mark_task_as_complete(self):
        self.task_service.add_task("Test task", "Test description", datetime.now() + timedelta(days=1))
        self.task_service.mark_task_as_complete(1)
        self.assertEqual(self.task_service.tasks[0].status, "Completed")

    def test_get_due_tasks(self):
        self.task_service.add_task("Due task", "Test description", datetime.now() - timedelta(days=1))
        due_tasks = self.task_service.get_due_tasks()
        self.assertEqual(len(due_tasks), 1)

if __name__ == "__main__":
    unittest.main()
