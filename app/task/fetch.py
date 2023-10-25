from app.task.model import Task
from app.user.auth import validate_user
from flask import make_response, jsonify


def get_tasks(auth: str):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        my_tasks = Task.objects(task_created_by=user)
        task_list = []
        for task in my_tasks:
            task = task.to_mongo().to_dict()
            task["id"] = str(task["id"])
            task_list.append(task)
        message = {"tasks": task_list}
        status_code = 200
    except Exception as err:
        message = {"message": "Task Fetch Failed"}
        status_code = 500
    return make_response(jsonify(message), status_code)


def get_task_details(auth: str, task_id: str):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        task = Task.objects(id=task_id).first()
        if task is None:
            return make_response(jsonify({"message": "Task not found"}), 404)
        if not task.task_created_by == user:
            return make_response(
                jsonify({"message": "Not authorized to view task details"}), 401
            )
        task = task.to_mongo().to_dict()
        task["id"] = str(task["id"])
        message = {"task": task}
        status_code = 200
    except Exception as err:
        message = {"message": "Task Detail Fetch Failed"}
        status_code = 500
    return make_response(jsonify(message), status_code)
