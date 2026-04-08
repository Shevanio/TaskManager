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

    def __init__(self):
        self.tasks = []
        self.next_id = 1
        pass

    def add_task(self, description):
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        print (f"Added task: {task}")
        return task

    def complete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completed = True
                print (f"Completed task: {task}")
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
                return task
        print (f"Task with id {id} not found.")
        return None
