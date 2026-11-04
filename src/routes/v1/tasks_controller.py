import logging

from flask import jsonify, make_response, request
from flask.views import MethodView

from src.db.database import SessionLocal
from src.services.task_services import TaskService

logger = logging.getLogger(__name__)


class TaskController(MethodView):
    def __init__(
        self,
    ):
        self.db = SessionLocal()

    def post(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            logger.warning("POST /v1/tasks rejeitado: corpo JSON ausente ou inválido")
            response = jsonify({"error": "Envie um objeto JSON válido"})
            return make_response(response, 406)

        with self.db as db:
            task_service = TaskService(db)
            stmt = task_service.create_task(data)

            response = jsonify(stmt.model_dump(mode="json"))
            return make_response(response, 201)

    def get(self):
        data = jsonify({"message": "Task Test"})
        return make_response(data, 200)

    def patch(self):
        data = jsonify({"message": "Task updated"})
        return make_response(data, 200)

    def delete(self):
        # data = jsonify({"message": "Task deleted"})
        return make_response("", 204)
