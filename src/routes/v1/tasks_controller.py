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

    def get(self, task_id: int | None = None):
        with self.db as db:
            task_service = TaskService(db)

            try:
                if task_id is not None:
                    task = task_service.get_task_by_id(task_id)
                    response = jsonify(task.model_dump(mode="json"))
                else:
                    raw_user_id = request.args.get("user_id")
                    if raw_user_id is None:
                        return make_response(
                            jsonify({"error": "Informe o parâmetro user_id"}),
                            400,
                        )

                    try:
                        user_id = int(raw_user_id)
                    except ValueError:
                        return make_response(
                            jsonify(
                                {"error": "O parâmetro user_id deve ser um inteiro"}
                            ),
                            400,
                        )

                    raw_status = request.args.get("completed")
                    if raw_status is None:
                        tasks = task_service.get_by_user(user_id)
                    else:
                        normalized_status = raw_status.lower()
                        if normalized_status not in {"true", "false"}:
                            return make_response(
                                jsonify(
                                    {
                                        "error": (
                                            "O parâmetro completed deve ser "
                                            "'true' ou 'false'"
                                        )
                                    }
                                ),
                                400,
                            )

                        tasks = task_service.get_by_status(
                            user_id,
                            normalized_status == "true",
                        )

                    response = jsonify([task.model_dump(mode="json") for task in tasks])

                logger.info("GET /v1/tasks concluído com sucesso")
                return make_response(response, 200)

            except ValueError as exc:
                logger.warning(f"GET /v1/tasks rejeitado: {exc}")
                return make_response(jsonify({"error": str(exc)}), 404)

    def patch(self):
        data = jsonify({"message": "Task updated"})
        return make_response(data, 200)

    def delete(self):
        # data = jsonify({"message": "Task deleted"})
        return make_response("", 204)
