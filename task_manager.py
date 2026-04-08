from fileinput import filename
import json

class Task:
    
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed
        pass

    def __str__(self):
        status = "✅" if self.completed else ""
        return f"[{status}] #{self.id} {self.description}" 

class TaskManager:
    FILENAME = "tasks.json"

    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def add_task(self, description):
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        print (f"Added task: {task}")
        self.save_tasks()
        return task

    def complete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completed = True
                print (f"Completed task: {task}")
                self.save_tasks()
                return task
        print (f"Task with id {id} not found.")
        return None

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for task in self.tasks:
                print(task)
        return self.tasks

    def delete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                print (f"Deleted task: {task}")
                self.save_tasks()
                return task
        print (f"Task with id {id} not found.")
        return None

    def save_tasks(self):
        with open(self.FILENAME, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open(self.FILENAME, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**data) for data in tasks_data]
                self.next_id = max(task.id for task in self.tasks) + 1 if self.tasks else 1
        except FileNotFoundError:
            print (f"No file named {self.FILENAME} found. Starting with an empty task list.")

    def update_tasks(self):
        self.load_tasks()
        print("Tasks updated from file.")