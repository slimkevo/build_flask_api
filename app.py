class Task:
    def __init__(self, task_id, title, description, completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []  # Placeholder for tasks, replace with a database in a real-world scenario

# Default route
@app.route('/')
def welcome():
    return jsonify({'message': 'Welcome to the Task Management API!'})

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(len(tasks) + 1, data['title'], data['description'])
    tasks.append(new_task)
    return jsonify({'message': 'Task created successfully', 'task_id': new_task.task_id}), 201

# Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({'tasks': [{'id': task.task_id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]})

# Retrieve a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = next((task for task in tasks if task.task_id == task_id), None)
    if task:
        return jsonify({'id': task.task_id, 'title': task.title, 'description': task.description, 'completed': task.completed})
    return jsonify({'message': 'Task not found'}), 404

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task.task_id == task_id), None)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        return jsonify({'message': 'Task updated successfully'})
    return jsonify({'message': 'Task not found'}), 404

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.task_id != task_id]
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True) 