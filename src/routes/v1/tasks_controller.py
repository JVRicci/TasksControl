import logging

from flask import jsonify, make_response, request
from flask.views import MethodView
from pydantic import ValidationError

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

        with self.db as db:
            task_service = TaskService(db)

            try:
                stmt = task_service.create_task(data)

                response = jsonify(stmt.model_dump(mode="json"))

                logger.info(f"POST /v1/tasks : tarefa {response} criado com sucesso")
                return make_response(response, 201)

            except ValidationError as exc:
                response = jsonify(
                    {
                        "error": "Dados inválidos",
                        "details": exc.errors(include_url=False),
                    }
                )

                logger.warning(f"POST /v1/tasks rejected: {exc.errors()}")
                return make_response(response, 400)

            except ValueError as exc:
                response = jsonify({"error": str(exc)})

                logger.warning(f"POST /v1/tasks rejected: {exc.errors()}")
                return make_response(response, 404)

    def get(self):
        data = jsonify({"message": "Task Test"})
        return make_response(data, 200)

    def patch(self):
        data = jsonify({"message": "Task updated"})
        return make_response(data, 200)

    def delete(self):
        # data = jsonify({"message": "Task deleted"})
        return make_response("", 204)
