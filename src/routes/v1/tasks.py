from flask import jsonify, make_response, request
from flask.views import MethodView


class Task(MethodView):
    def get(self):
        data = jsonify({"message": "Task Test"})
        return make_response(data, 200)

    def post(self):
        idempotency_key = request.header
        data = jsonify({"message": "Task Created"})
        return make_response(data, 201)

    def patch(self):
        data = jsonify({"message": "Task updated"})
        return make_response(data, 200)

    def delete(self):
        # data = jsonify({"message": "Task deleted"})
        return make_response("", 204)
