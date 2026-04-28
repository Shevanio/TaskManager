# 📋 TaskManager

A modern task manager with AI integration to automatically break complex tasks down into simple, actionable subtasks.

## ✨ Features

- **Complete task management**: Add, list, complete, and delete tasks
- **Smart AI decomposition**: Uses OpenAI to break complex tasks into subtasks
- **Data persistence**: Automatic JSON storage
- **Interactive interface**: Intuitive CLI menu for operations
- **Task status tracking**: Mark tasks as completed with a visual indicator (✅)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- OpenAI API key (for AI features)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd TaskManager
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Usage

```bash
python main.py
```

An interactive menu will open with the following options:

```
 --- Task Manager --- 

1. Add Task                    # Add a simple task
2. Add complex Task (using AI) # Break down a task with AI
3. Complete Task               # Mark a task as completed
4. List Tasks                  # View all tasks
5. Delete Task                 # Delete a task
6. Update Tasks                # Reload tasks from file
7. Exit                        # Exit
```

## 📖 Usage Examples

### Add a simple task
```
Enter your choice: 1
Enter task description: Buy milk
Added task: [] #1 Buy milk
```

### Break down a complex task with AI
```
Enter your choice: 2
Enter complex task description: Organize a tech conference
```

The AI will break it down into subtasks such as:
- Select venue and date
- Confirm speakers and agenda
- Organize logistics and catering
- Promote the event and manage attendee registration

These will be added automatically as tasks.

### List tasks
```
Enter your choice: 4
[] #1 Buy milk
[✅] #2 Select venue and date
[] #3 Confirm speakers and agenda
```

### Complete a task
```
Enter your choice: 3
Enter task id to complete: 1
Completed task: [✅] #1 Buy milk
```

## 🏗️ Project Structure

```
TaskManager/
├── main.py                    # Entry point and CLI interface
├── task_manager.py            # TaskManager and Task classes
├── ai_service.py              # OpenAI integration
├── tasks.json                 # Task storage (generated)
├── requirements.txt           # Project dependencies
├── test_comprehensive.py      # Full test suite
├── test.py                    # Basic tests
└── README.md                  # This file
```

## 🔌 API

### Task class

```python
task = Task(id, description, completed=False)

# Attributes
task.id           # int: Unique task ID
task.description  # str: Task description
task.completed    # bool: Completion status

# Methods
str(task)         # str: String representation with status emoji
```

### TaskManager class

```python
manager = TaskManager()

# Methods
manager.add_task(description)          # Task: Add a new task
manager.complete_task(id)              # Task|None: Mark as completed
manager.list_tasks()                   # List[Task]: List all tasks
manager.delete_task(id)                # Task|None: Delete a task
manager.save_tasks()                   # None: Save to JSON
manager.load_tasks()                   # None: Load from JSON
manager.update_tasks()                 # None: Reload from file
```

### AI Service

```python
from ai_service import create_simple_tasks

# Break a task down into subtasks
subtasks = create_simple_tasks("Complex task here")
# Returns: List[str] of subtasks or an error

# Example
subtasks = create_simple_tasks("Plan a trip to Europe")
for subtask in subtasks:
    print(subtask)
```

**OpenAI API parameters used:**
- Model: `gpt-3.5-turbo`
- Temperature: `0.7` (moderate creativity)
- Max tokens: `300` (concise subtasks)

## 🧪 Testing

The project includes a full test suite with **30 test cases** covering:

### Run all tests
```bash
python -m unittest test_comprehensive -v
```

### Included test types

**Unit tests:**
- Task creation and representation
- TaskManager CRUD operations
- JSON persistence
- Error handling
- OpenAI integration

**Integration tests:**
- Full AI workflow
- Task lifecycle

## ⚙️ Configuration

### Environment variables (.env)

```env
OPENAI_API_KEY=your_api_key_here
```

**Note:** Never commit the `.env` file with your real key.

### Storage file (tasks.json)

Storage format:
```json
[
    {
        "id": 1,
        "description": "Buy milk",
        "completed": false
    },
    {
        "id": 2,
        "description": "Study Python",
        "completed": true
    }
]
```

## 🐛 Error Handling

- **API key not configured**: Raises `ValueError` if `OPENAI_API_KEY` is missing
- **API unavailable**: Returns an error message instead of crashing
- **Task ID not found**: Operations return `None` silently
- **Corrupted file**: Starts with an empty list

## 📋 Project Requirements

```
openai>=1.0.0
python-dotenv>=0.19.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🔐 Security

- ⚠️ Never hardcode your API key
- ⚠️ Use `.env` and never commit it
- ⚠️ Restrict `tasks.json` permissions if it contains sensitive data

## 🤝 Contributing

To contribute to the project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Development Notes

### Internal TaskManager structure

- Tasks are loaded into memory on startup
- They are persisted to `tasks.json` after each operation
- IDs are auto-incremented automatically
- State is preserved between sessions

### Future improvements

- [ ] Categories and tags for tasks
- [ ] Due dates
- [ ] Priorities
- [ ] Nested subtasks
- [ ] Database support (SQLite/PostgreSQL)
- [ ] REST API
- [ ] Web interface
- [ ] Multi-user support

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed as a demonstration tool for AI-assisted task management.

---

**Questions?** Check the tests in `test_comprehensive.py` to see more usage examples.
