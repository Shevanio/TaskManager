from task_manager import TaskManager
from ai_service import create_simple_tasks


def print_menu():
    print("\n --- Task Manager --- \n")

    print ("1. Add Task")
    print ("2. Add complex Task (using AI)")
    print ("3. Complete Task")
    print ("4. List Tasks")
    print ("5. Delete Task")
    print ("6. Update Tasks")
    print ("7. Exit")

def main():
    manager = TaskManager()

    while True:
        print_menu()

        try:
            choice = int(input("Enter your choice: "))

            match choice:
                case 1:
                    description = input("Enter task description: ")
                    manager.add_task(description)
                case 2:
                    description = input("Enter complex task description: ")
                    subtasks = create_simple_tasks(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break

                case 3:
                    id = int(input("Enter task id to complete: "))
                    manager.complete_task(id)
                case 4:
                    manager.list_tasks()
                case 5:
                    id = int(input("Enter task id to delete: "))
                    manager.delete_task(id)
                case 6:
                    print ("Updating tasks.")
                    manager.update_tasks()
                case 7:
                    print("Exiting...")
                    break
                case _:
                    print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()