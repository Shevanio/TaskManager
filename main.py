from task_manager import TaskManager

def print_menu():
    print("\n --- Task Manager --- \n")

    print ("1. Add Task")
    print ("2. Complete Task")
    print ("3. List Tasks")
    print ("4. Delete Task")
    print ("5. Update Tasks")
    print ("6. Exit")

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
                    id = int(input("Enter task id to complete: "))
                    manager.complete_task(id)
                case 3:
                    manager.list_tasks()
                case 4:
                    id = int(input("Enter task id to delete: "))
                    manager.delete_task(id)
                case 5:
                    manager.update_tasks()
                case 6:
                    print("Exiting...")
                    break
                case _:
                    print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()