from termcolor import colored
import re

# File to store tasks
TASKS_FILE = "tasks.txt"

# Global tasks list
tasks = []

# Function to validate task names
def validate_task_name(task_name):
    # Regex to allow letters, numbers, spaces, and punctuation like !, ?, ., commas, etc.
    if re.match("^[A-Za-z0-9\s,.'!?&$-]*$", task_name):
        return True
    return False

# Function to load tasks from the text file
def load_tasks():
    try:
        # Ensure the file exists and is created if missing
        open(TASKS_FILE, 'a').close()  # This will create the file if it doesn't exist
        # Attempt to open and read the tasks file
        with open(TASKS_FILE, "r") as file:
            tasks_data = file.readlines()
        # Convert each task into a dictionary with 'task', 'status', and 'importance'
        tasks = []
        for task in tasks_data:
            task_fields = task.strip().split('|')
            if len(task_fields) == 3:
                tasks.append({"task": task_fields[0], "status": task_fields[1], "importance": task_fields[2]})
            else:
                print(colored(f"Skipping invalid task entry: {task}", 'red'))
        return tasks
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []

# Function to save tasks to the text file
def save_tasks():
    try:
        # Open the file in write mode and save all tasks to it
        with open(TASKS_FILE, "w") as file:
            for task in tasks:
                # Save each task with 'task|status|importance'
                file.write(f"{task['task']}|{task['status']}|{task['importance']}\n")
    except Exception as e:
        # If there's any error during saving, print it out
        print(f"Error saving tasks: {e}")

# Function to display the menu options
def display_menu():
    print("\nWelcome to the To-Do List Application!")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Mark Task as Done")
    print("5. Change Task Importance")
    print("6. Remove All Done Tasks")
    print("7. Quit")

# Function to get valid task number input
def get_valid_task_number():
    while True:
        try:
            task_number = int(input("Enter the task number: "))
            if task_number < 1 or task_number > len(tasks):
                print(colored("Task number out of range. Please enter a valid number.", 'red'))
            else:
                return task_number
        except ValueError:
            print(colored("Invalid input. Please enter a valid number.", 'red'))

# Function to add a new task
def add_task():
    task_name = input("Enter the task to add: ")

    # Validate task name
    if not validate_task_name(task_name):
        print(colored("Invalid task name. Please use only valid characters.", 'red'))
        return
    
    # Show options for importance
    print("\nChoose the importance level:")
    print("1. High")
    print("2. Medium")
    print("3. Low")
    importance_choice = input("Enter the number corresponding to importance: ")
    
    # Validate input for importance choice
    while importance_choice not in ['1', '2', '3']:
        importance_choice = input("Please enter a valid number (1 for High, 2 for Medium, 3 for Low): ")
    
    # Map the number to importance
    importance = {'1': 'High', '2': 'Medium', '3': 'Low'}[importance_choice]

    # Add the new task with a 'Pending' status to the list
    tasks.append({"task": task_name, "status": "Pending", "importance": importance})
    # Save the updated tasks back to the file
    save_tasks()
    # Notify the user of the successful addition
    print(colored(f"Task '{task_name}' added successfully!", 'green'))

# Function to view all tasks
def view_tasks():
    if len(tasks) == 0:
        # If there are no tasks, show this message
        print(colored("Nothing to do yet. Tell me what you need to get done...", 'yellow'))
    else:
        # Sort tasks by importance (High > Medium > Low)
        importance_order = {'High': 3, 'Medium': 2, 'Low': 1}
        tasks_sorted = sorted(tasks, key=lambda x: importance_order[x['importance']], reverse=True)

        print("\nYour Tasks:")
        for index, task in enumerate(tasks_sorted, start=1):
            # Color the task's status (red for pending, green for done)
            status_color = 'red' if task['status'] == 'Pending' else 'green'
            print(f"{index}. {colored(task['task'], 'cyan')} "
                  f"[{colored(task['status'], status_color)}] - Importance: {colored(task['importance'], 'magenta')}")

# Function to delete a task
def delete_task():
    task_number = input("Enter the task number to delete or type 'ALL' to delete all tasks: ")

    if task_number == "ALL":
        # Ask for confirmation before deleting all tasks
        confirm = input("Are you sure you want to delete all tasks? This action cannot be undone (yes/no): ").lower()
        if confirm == 'yes':
            tasks.clear()  # Clear the tasks list
            save_tasks()  # Save the empty list back to the file
            print(colored("All tasks have been deleted.", 'red'))
        else:
            print(colored("Action cancelled. No tasks were deleted.", 'yellow'))
    else:
        try:
            task_number = int(task_number)
            if task_number < 1 or task_number > len(tasks):
                raise IndexError("Task number out of range.")
            deleted_task = tasks.pop(task_number - 1)
            save_tasks()  # Save the updated list of tasks back to the file
            print(colored(f"Task '{deleted_task['task']}' deleted successfully!", 'red'))
        except ValueError:
            print(colored("Invalid input. Please enter a valid task number or 'ALL' to delete all tasks.", 'red'))
        except IndexError:
            print(colored("No task exists with that number.", 'red'))

# Function to mark a task as done
def mark_done():
    task_number = get_valid_task_number()
    task = tasks[task_number - 1]
    task['status'] = 'Done'
    save_tasks()  # Save the updated tasks to the file
    print(colored(f"Task '{task['task']}' marked as Done.", 'green'))

# Function to change the importance of a task
def change_importance():
    task_number = get_valid_task_number()
    task = tasks[task_number - 1]
    
    # Show options for importance
    print("\nChoose the new importance level:")
    print("1. High")
    print("2. Medium")
    print("3. Low")
    importance_choice = input("Enter the number corresponding to importance: ")
    
    # Validate input for importance choice
    while importance_choice not in ['1', '2', '3']:
        importance_choice = input("Please enter a valid number (1 for High, 2 for Medium, 3 for Low): ")
    
    task['importance'] = {'1': 'High', '2': 'Medium', '3': 'Low'}[importance_choice]
    
    save_tasks()  # Save the updated tasks to the file
    print(colored(f"Task '{task['task']}' importance changed to {task['importance']}.", 'green'))

# Function to remove all tasks marked as "Done"
def remove_done_tasks():
    global tasks
    tasks = [task for task in tasks if task['status'] != 'Done']
    save_tasks()  # Save the updated tasks to the file
    print(colored("All done tasks have been removed.", 'green'))

# Main function to run the program
def main():
    global tasks
    # Load tasks when the script starts
    tasks = load_tasks()
    
    # Show tasks or a message if empty before displaying the menu
    view_tasks()

    while True:
        # Display the menu for the user to choose from
        display_menu()
        
        try:
            # Capture the user's menu choice
            user_choice = int(input("Choose an option (1-7): "))
            
            if user_choice == 1:
                # If the user chooses to add a task
                add_task()
            elif user_choice == 2:
                # If the user wants to view tasks
                view_tasks()
            elif user_choice == 3:
                # If the user wants to delete a task or all tasks
                delete_task()
            elif user_choice == 4:
                # If the user wants to mark a task as done
                mark_done()
            elif user_choice == 5:
                # If the user wants to change the importance of a task
                change_importance()
            elif user_choice == 6:
                # If the user wants to remove all done tasks
                remove_done_tasks()
            elif user_choice == 7:
                # If the user wants to quit
                print(colored("Goodbye!", 'blue'))
                break
            else:
                print(colored("Invalid choice. Please select a valid option.", 'red'))
        except ValueError:
            print(colored("Invalid input. Please enter a number between 1 and 7.", 'red'))

# Run the application if this is the main script
if __name__ == "__main__":
    main()
