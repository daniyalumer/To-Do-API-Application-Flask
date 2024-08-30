from flask import Flask, jsonify, request
from datetime import datetime
import hashlib

app = Flask(__name__)

todo_list = []


def generatehash(description):
    return hashlib.md5(description.encode("utf-8")).hexdigest()

def get_current_time():
    return str(datetime.now)[:-7]

@app.route('/todos', methods=['GET'])
def gettodos():
    return jsonify({"todo-list":todo_list}), 200

@app.route("/todo", methods=["POST"])
def create_or_update_todo():
    # TODO: should be coming from the request body instead
    request_data=request.get_json()
    description = request_data.get('description')
    id = request_data.get('id', None)
    current_time = str(datetime.now())[:-7]
    completed=request_data.get('completed', False)

    # mark as completed
    if completed:
        for todo in todo_list:
            if todo["id"] == id:
                todo["completed"] = True
                todo["date_completed"] = current_time
                return jsonify({"message": "Item marked as completed", "todo": todo}), 200
        return jsonify({"error": "Todo item not found"}), 404

    # TabularJSON.com
    # Postman application

    # update item
    if id:
        for todo in todo_list:
            if id == todo["id"]:
                todo["id"] = generatehash(description)
                todo["description"] = description
                todo["dateupdated"] = current_time
                return jsonify({'message': f'Item {id} updated successfully', 'todo': todo}), 200
        return jsonify({"error": "Todo item not found"}), 404

    # create item
    else:
        todo_id = generatehash(description)
        for todo in todo_list:
            if todo["id"] == todo_id:
                return jsonify({"error": "Item with the same description already exists"}), 400

        new_todo_item = {
            "id": todo_id,
            "description": description,
            "date_created": current_time,
            "date_updated": current_time,
            "date_completed": None,
            "completed": False,
        }
        todo_list.append(new_todo_item)
        return jsonify({'message': 'New item created in to-do list', 'todo': new_todo_item}), 201


# this should be done in the /todo POST updation block
""" @app.route("/completed/<string:todo_id>", methods=["POST"])
def completed_todo_by_id(todo_id):
    current_time = str(datetime.now())[0:7]
    for todo in todo_list:
        if todo["id"] == todo_id:
            todo["completed"] = (True,)
            todo["date_completed"] = current_time
            return redirect(url_for("home"))
    return jsonify({"error": "Todo item not found"}), 404 """



if __name__ == "__main__":
    app.run(debug=True)
