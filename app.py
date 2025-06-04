from flask import Flask, request, redirect, url_for, render_template_string
import json
from pathlib import Path

DATA_FILE = Path('todos.json')

app = Flask(__name__)

def load_todos():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

todos = load_todos()

HTML_TEMPLATE = """
<!doctype html>
<title>Todo App</title>
<h1>Todo List</h1>
<form action="/add" method="post">
  <input type="text" name="task" placeholder="New task" required>
  <button type="submit">Add</button>
</form>
<ul>
{% for todo in todos %}
  <li>
    {{ todo['task'] }}
    <a href="/delete/{{ loop.index0 }}">delete</a>
  </li>
{% endfor %}
</ul>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    todos.append({'task': task})
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:idx>')
def delete(idx):
    if 0 <= idx < len(todos):
        todos.pop(idx)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
