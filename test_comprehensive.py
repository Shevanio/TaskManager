import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from task_manager import TaskManager, Task
from ai_service import create_simple_tasks


class TestTask(unittest.TestCase):
    """Tests for the Task class."""

    def test_task_creation(self):
        """Test creating a Task with default parameters."""
        task = Task(1, "Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Buy groceries")
        self.assertFalse(task.completed)

    def test_task_creation_with_completed(self):
        """Test creating a Task with completed status."""
        task = Task(2, "Finish project", completed=True)
        self.assertEqual(task.id, 2)
        self.assertEqual(task.description, "Finish project")
        self.assertTrue(task.completed)

    def test_task_str_incomplete(self):
        """Test string representation of incomplete task."""
        task = Task(1, "Buy groceries", completed=False)
        result = str(task)
        self.assertIn("#1", result)
        self.assertIn("Buy groceries", result)
        self.assertNotIn("✅", result)

    def test_task_str_completed(self):
        """Test string representation of completed task."""
        task = Task(1, "Buy groceries", completed=True)
        result = str(task)
        self.assertIn("#1", result)
        self.assertIn("Buy groceries", result)
        self.assertIn("✅", result)


class TestTaskManager(unittest.TestCase):
    """Tests for the TaskManager class."""

    def setUp(self):
        """Create a temporary directory and set up TaskManager."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.manager = TaskManager()

    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        if os.path.exists(os.path.join(self.test_dir, TaskManager.FILENAME)):
            os.remove(os.path.join(self.test_dir, TaskManager.FILENAME))
        os.rmdir(self.test_dir)

    def test_taskmanager_initialization(self):
        """Test TaskManager initializes with empty task list."""
        self.assertEqual(self.manager.tasks, [])
        self.assertEqual(self.manager.next_id, 1)

    def test_add_task_single(self):
        """Test adding a single task."""
        task = self.manager.add_task("Buy groceries")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Buy groceries")
        self.assertFalse(task.completed)

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks with auto-incrementing IDs."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        task3 = self.manager.add_task("Task 3")

        self.assertEqual(len(self.manager.tasks), 3)
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        self.assertEqual(self.manager.next_id, 4)

    def test_list_tasks_empty(self):
        """Test listing tasks when no tasks exist."""
        result = self.manager.list_tasks()
        self.assertEqual(result, [])

    def test_list_tasks_with_data(self):
        """Test listing tasks when tasks exist."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        result = self.manager.list_tasks()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].description, "Task 1")
        self.assertEqual(result[1].description, "Task 2")

    def test_complete_task_existing(self):
        """Test completing an existing task."""
        task = self.manager.add_task("Buy groceries")
        result = self.manager.complete_task(1)

        self.assertIsNotNone(result)
        self.assertTrue(result.completed)
        self.assertEqual(result.id, 1)

    def test_complete_task_nonexistent(self):
        """Test completing a task that doesn't exist."""
        self.manager.add_task("Task 1")
        result = self.manager.complete_task(999)
        self.assertIsNone(result)

    def test_complete_task_mark_as_complete(self):
        """Test that completing a task updates the task object."""
        self.manager.add_task("Task 1")
        self.assertFalse(self.manager.tasks[0].completed)
        self.manager.complete_task(1)
        self.assertTrue(self.manager.tasks[0].completed)

    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        result = self.manager.delete_task(1)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].id, 2)

    def test_delete_task_nonexistent(self):
        """Test deleting a task that doesn't exist."""
        self.manager.add_task("Task 1")
        result = self.manager.delete_task(999)
        self.assertIsNone(result)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_save_tasks(self):
        """Test that tasks are saved to JSON file correctly."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.complete_task(1)

        # Verify file exists
        self.assertTrue(os.path.exists(TaskManager.FILENAME))

        # Verify file contents
        with open(TaskManager.FILENAME, 'r') as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['description'], "Task 1")
        self.assertTrue(data[0]['completed'])
        self.assertEqual(data[1]['id'], 2)
        self.assertFalse(data[1]['completed'])

    def test_load_tasks_from_file(self):
        """Test loading tasks from an existing JSON file."""
        # Create a new manager and add tasks
        manager1 = TaskManager()
        manager1.add_task("Saved Task 1")
        manager1.add_task("Saved Task 2")
        manager1.complete_task(1)

        # Create a new manager and verify it loads the tasks
        manager2 = TaskManager()
        self.assertEqual(len(manager2.tasks), 2)
        self.assertEqual(manager2.tasks[0].description, "Saved Task 1")
        self.assertTrue(manager2.tasks[0].completed)
        self.assertEqual(manager2.tasks[1].description, "Saved Task 2")
        self.assertFalse(manager2.tasks[1].completed)

    def test_load_tasks_empty_file(self):
        """Test loading from a non-existent file."""
        # Create a fresh manager (should not raise an error)
        manager = TaskManager()
        self.assertEqual(len(manager.tasks), 0)
        self.assertEqual(manager.next_id, 1)

    def test_next_id_after_load(self):
        """Test that next_id is set correctly after loading from file."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")

        # Load from file
        manager2 = TaskManager()
        self.assertEqual(manager2.next_id, 4)

    def test_update_tasks_reloads_from_file(self):
        """Test that update_tasks reloads from file."""
        self.manager.add_task("Original Task")

        # Manually modify the file
        with open(TaskManager.FILENAME, 'w') as f:
            json.dump([
                {"id": 1, "description": "Modified Task", "completed": False}
            ], f)

        # Update should reload
        self.manager.update_tasks()
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].description, "Modified Task")

    def test_complete_and_delete_workflow(self):
        """Test a workflow of adding, completing, and deleting tasks."""
        # Add tasks
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")

        # Complete Task 1
        self.manager.complete_task(1)
        self.assertTrue(self.manager.tasks[0].completed)

        # Delete Task 2
        self.manager.delete_task(2)
        self.assertEqual(len(self.manager.tasks), 2)

        # Verify remaining tasks
        self.assertEqual(self.manager.tasks[0].id, 1)
        self.assertEqual(self.manager.tasks[1].id, 3)


class TestAIService(unittest.TestCase):
    """Tests for the AI service functionality."""

    @patch("ai_service.client")
    def test_create_simple_tasks_success(self, mock_client):
        """Test successful task decomposition with valid API response."""
        # Arrange
        description = "Organizar una conferencia"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "- Seleccionar ubicación\n"
            "- Confirmar speakers\n"
            "- Organizar logística"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        # Act
        result = create_simple_tasks(description)

        # Assert
        self.assertEqual(len(result), 3)
        self.assertIn("Seleccionar ubicación", result)
        self.assertIn("Confirmar speakers", result)
        self.assertIn("Organizar logística", result)

    @patch("ai_service.client")
    def test_create_simple_tasks_with_extra_whitespace(self, mock_client):
        """Test parsing with extra whitespace."""
        description = "Test task"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "-   Subtarea 1   \n"
            "-Subtarea 2\n"
            "-  Subtarea 3  "
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        result = create_simple_tasks(description)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Subtarea 1")
        self.assertEqual(result[1], "Subtarea 2")
        self.assertEqual(result[2], "Subtarea 3")

    @patch("ai_service.client")
    def test_create_simple_tasks_no_valid_lines(self, mock_client):
        """Test fallback when response has no dash-prefixed lines."""
        description = "Test task"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Esta respuesta no tiene guiones"
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        result = create_simple_tasks(description)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Error: No se pudieron generar subtareas.")

    @patch("ai_service.client")
    def test_create_simple_tasks_empty_response(self, mock_client):
        """Test handling of empty API response."""
        description = "Test task"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = ""
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        result = create_simple_tasks(description)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Error: No se pudieron generar subtareas.")

    @patch("ai_service.client")
    def test_create_simple_tasks_api_exception(self, mock_client):
        """Test error handling when API raises exception."""
        description = "Test task"
        mock_client.chat.completions.create.side_effect = Exception("Connection failed")
        mock_client.api_key = "test-key"

        result = create_simple_tasks(description)

        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].startswith("Error:"))
        self.assertIn("Connection failed", result[0])

    @patch("ai_service.client")
    def test_create_simple_tasks_no_api_key(self, mock_client):
        """Test that error is raised when API key is missing."""
        mock_client.api_key = None

        with self.assertRaises(ValueError) as context:
            create_simple_tasks("Any description")

        self.assertIn("OpenAI API key not found", str(context.exception))

    @patch("ai_service.client")
    def test_create_simple_tasks_api_called_with_correct_params(self, mock_client):
        """Test that API is called with expected parameters."""
        description = "Sample task"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "- Task 1\n- Task 2"
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        create_simple_tasks(description)

        # Verify API was called
        mock_client.chat.completions.create.assert_called_once()

        # Verify parameters
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs["model"], "gpt-3.5-turbo")
        self.assertEqual(call_kwargs["temperature"], 0.7)
        self.assertEqual(call_kwargs["max_tokens"], 300)
        self.assertIn("Sample task", call_kwargs["messages"][1]["content"])

    @patch("ai_service.client")
    def test_create_simple_tasks_mixed_content(self, mock_client):
        """Test parsing with mixed content (dashes and non-dashes)."""
        description = "Test task"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "Aquí hay las subtareas:\n"
            "- Subtarea 1\n"
            "Esto no empieza con guión\n"
            "- Subtarea 2\n"
            "Otra línea\n"
            "- Subtarea 3"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        result = create_simple_tasks(description)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Subtarea 1")
        self.assertEqual(result[1], "Subtarea 2")
        self.assertEqual(result[2], "Subtarea 3")


class TestIntegration(unittest.TestCase):
    """Integration tests combining TaskManager and AI Service."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.manager = TaskManager()

    def tearDown(self):
        """Clean up."""
        os.chdir(self.original_cwd)
        if os.path.exists(os.path.join(self.test_dir, TaskManager.FILENAME)):
            os.remove(os.path.join(self.test_dir, TaskManager.FILENAME))
        os.rmdir(self.test_dir)

    @patch("ai_service.client")
    def test_add_subtasks_from_ai(self, mock_client):
        """Test adding subtasks generated by AI service."""
        # Mock AI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "- Subtarea 1\n"
            "- Subtarea 2\n"
            "- Subtarea 3"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        # Get AI-generated subtasks
        subtasks = create_simple_tasks("Complex task")

        # Add them to TaskManager
        for subtask in subtasks:
            if not subtask.startswith("Error:"):
                self.manager.add_task(subtask)

        # Verify they were added
        self.assertEqual(len(self.manager.tasks), 3)
        self.assertEqual(self.manager.tasks[0].description, "Subtarea 1")
        self.assertEqual(self.manager.tasks[1].description, "Subtarea 2")
        self.assertEqual(self.manager.tasks[2].description, "Subtarea 3")

    @patch("ai_service.client")
    def test_complete_all_ai_generated_subtasks(self, mock_client):
        """Test a workflow: generate subtasks, add them, and complete all."""
        # Mock AI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "- Step 1\n"
            "- Step 2\n"
            "- Step 3"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key"

        # Generate and add subtasks
        subtasks = create_simple_tasks("Project")
        for subtask in subtasks:
            if not subtask.startswith("Error:"):
                self.manager.add_task(subtask)

        # Complete all tasks
        for task in self.manager.tasks:
            self.manager.complete_task(task.id)

        # Verify all are completed
        results = self.manager.list_tasks()
        for task in results:
            self.assertTrue(task.completed)


if __name__ == "__main__":
    unittest.main()
