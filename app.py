from flask import Flask, request, jsonify
from models import db, Todo
from config import Config
import logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configure the app with settings from config.py
app.config.from_object(Config)


# Initialize the database with connection pooling options
db.init_app(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/todo', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'description' not in data:
            return jsonify({"error": "Invalid data"}), 400
        
        new_todo = Todo(
            name=data['name'],
            description=data['description'],
            is_Completed=False
        )
        db.session.add(new_todo)
        db.session.commit()
        
        return jsonify({
            'id': new_todo.id,
            'name': new_todo.name,
            'description': new_todo.description,
            'created_at': new_todo.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': new_todo.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'is_Completed' : new_todo.is_Completed
        }), 201

    except SQLAlchemyError as e:
        logging.error("Database error occurred while creating todo: %s", str(e))
        db.session.rollback()  # Rollback the session to avoid any invalid state
        return jsonify({"error": "A database error occurred while creating the todo"}), 500

    except Exception as e:
        logging.error("Error occurred while creating todo: %s", str(e))
        return jsonify({"error": "An error occurred while creating the todo"}), 500
    

@app.route('/todo', methods=['GET'])
def get_todos():
    try:
        # Get query parameter
        updated_after = request.args.get('updated_after')

        # Query todos
        query = Todo.query
        if updated_after:
            try:
                updated_after_date = datetime.fromisoformat(updated_after)
                query = query.filter(Todo.updated_at >= updated_after_date)
            except ValueError:
                return jsonify({"error": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

        todos = query.all()

        # Serialize the todos data
        serialized_todos = []
        for todo in todos:
            serialized_todos.append({
                'id': todo.id,
                'name': todo.name,
                'description': todo.description,
                'created_at': todo.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': todo.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'is_Completed' : todo.is_Completed
            })

        return jsonify(serialized_todos), 200

    except SQLAlchemyError as e:
        logging.error("Database error occurred while fetching todos: %s", str(e))
        return jsonify({"error": "A database error occurred while fetching todos"}), 500

    except Exception as e:
        logging.error("Error occurred while fetching todos: %s", str(e))
        return jsonify({"error": "An error occurred while fetching todos"}), 500



@app.route('/todo/<ulid>', methods=['PUT'])
def update_todo(ulid):
    try:
        # Find the todo by ULID
        todo = Todo.query.filter_by(id=ulid).first()

        if not todo:
            return jsonify({"error": "Todo not found"}), 404

        # Get changes from query parameters
        name = request.args.get('name', todo.name)
        description = request.args.get('description', todo.description)
        is_Completed = request.args.get('is_Completed', todo.is_Completed)

        if is_Completed is not None:
            if is_Completed.lower() == 'true':
                is_Completed = True
            elif is_Completed.lower() == 'false':
                is_Completed = False
            else:
                return jsonify({"error": "Invalid value for is_Completed"}), 400
        else:
            is_Completed = todo.is_Completed

        # Update todo with new values
        todo.name = name
        todo.description = description
        todo.is_Completed = is_Completed
        todo.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'id': todo.id,
            'name': todo.name,
            'description': todo.description,
            'created_at': todo.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': todo.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'is_Completed' : todo.is_Completed
        }), 200

    except SQLAlchemyError as e:
        logging.error("Database error occurred while updating todo: %s", str(e))
        db.session.rollback()  # Rollback the session to avoid any invalid state
        return jsonify({"error": "A database error occurred while updating the todo"}), 500

    except Exception as e:
        logging.error("Error occurred while updating todo: %s", str(e))
        return jsonify({"error": "An error occurred while updating the todo"}), 500



@app.route('/todo/<ulid>', methods=['DELETE'])
def delete_todo(ulid):
    try:
        # Find the todo by ULID
        todo = Todo.query.filter_by(id=ulid).first()

        if not todo:
            return jsonify({"error": "Todo not found"}), 404

        # Delete the todo from the database
        db.session.delete(todo)
        db.session.commit()

        return jsonify({"message": "Todo deleted successfully"}), 200

    except SQLAlchemyError as e:
        logging.error("Database error occurred while deleting todo: %s", str(e))
        db.session.rollback()  # Rollback the session to avoid any invalid state
        return jsonify({"error": "A database error occurred while deleting the todo"}), 500

    except Exception as e:
        logging.error("Error occurred while deleting todo: %s", str(e))
        return jsonify({"error": "An error occurred while deleting the todo"}), 500


if __name__ == '__main__':
    app.run(debug=True)
