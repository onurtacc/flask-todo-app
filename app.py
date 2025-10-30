from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

swagger = Swagger(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if title:
        todo = Todo(title=title, complete=False)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/incomplete/<int:todo_id>")
def incomplete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    new_title = request.form.get("title")
    if new_title:
        todo.title = new_title
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/api/todos", methods=["GET"])
def api_get_todos():
    """
    Get all todos
    ---
    responses:
      200:
        description: List of todo items
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "Buy groceries"
              complete:
                type: boolean
                example: false
    """
    todos = Todo.query.all()
    return jsonify([{"id": t.id, "title": t.title, "complete": t.complete} for t in todos])

@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def api_get_todo(todo_id):
    """
    Get todo by ID
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
        description: ID of the todo item
        example: 1
    responses:
      200:
        description: A todo item
        schema:
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: "Buy groceries"
            complete:
              type: boolean
              example: false
      404:
        description: Todo not found
    """
    todo = Todo.query.get_or_404(todo_id)
    return jsonify({"id": todo.id, "title": todo.title, "complete": todo.complete})

@app.route("/api/todos", methods=["POST"])
def api_create_todo():
    """
    Create a new todo
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            title:
              type: string
              example: "New task"
    responses:
      201:
        description: Todo created successfully
        schema:
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: "New task"
            complete:
              type: boolean
              example: false
      400:
        description: Invalid input
    """
    if not request.is_json:
        return jsonify({"error": "Missing JSON"}), 400
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    todo = Todo(title=title, complete=False)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "complete": todo.complete}), 201

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def api_update_todo(todo_id):
    """
    Update a todo by ID
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
        description: ID of the todo to update
        example: 1
      - in: body
        name: body
        required: true
        schema:
          properties:
            title:
              type: string
              example: "Updated task"
            complete:
              type: boolean
              example: true
    responses:
      200:
        description: Updated todo item
        schema:
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: "Updated task"
            complete:
              type: boolean
              example: true
      400:
        description: Invalid input
      404:
        description: Todo not found
    """
    todo = Todo.query.get_or_404(todo_id)
    if not request.is_json:
        return jsonify({"error": "Missing JSON"}), 400
    data = request.get_json()
    title = data.get("title")
    complete = data.get("complete")
    if title is None:
        return jsonify({"error": "Title is required"}), 400
    todo.title = title
    if isinstance(complete, bool):
        todo.complete = complete
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "complete": todo.complete})

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    """
    Delete a todo by ID
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
        description: ID of the todo to delete
        example: 1
    responses:
      200:
        description: Deletion result
        schema:
          properties:
            result:
              type: boolean
              example: true
      404:
        description: Todo not found
    """
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"result": True})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
