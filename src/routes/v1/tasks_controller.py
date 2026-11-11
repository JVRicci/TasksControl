import logging

from flask import jsonify, make_response, request
from flask.views import MethodView
from pydantic import ValidationError

from src.db.database import SessionLocal
from src.schemas.task_query_schema import TaskQuerySchema
from src.services.task_services import TaskService

logger = logging.getLogger(__name__)


class TaskController(MethodView):
    def __init__(
        self,
    ):
        self.session = SessionLocal()

    def post(self):
        data = request.get_json(silent=True)

        with self.session as session:
            task_service = TaskService(session)

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
        with self.session as session:
            task_service = TaskService(session)

            try:
                if task_id is not None:
                    task = task_service.get_task_by_id(task_id)
                    response = task.model_dump(mode="json")
                else:
                    query = TaskQuerySchema.model_validate(request.args.to_dict())

                    if query.completed is None:
                        tasks = task_service.get_by_user(query.user_id)
                    else:
                        tasks = task_service.get_by_status(
                            query.user_id,
                            query.completed,
                        )

                    response = [task.model_dump(mode="json") for task in tasks]

                logger.info("GET /v1/tasks concluído com sucesso")
                return make_response(jsonify(response), 200)

            except ValidationError as exc:
                logger.warning("GET /v1/tasks com parâmetros inválidos: %s", exc)
                return make_response(
                    jsonify(
                        {
                            "error": "Parâmetros inválidos",
                            "details": exc.errors(include_url=False),
                        }
                    ),
                    400,
                )

            except ValueError as exc:
                logger.warning("GET /v1/tasks rejeitado: %s", exc)
                return make_response(jsonify({"error": str(exc)}), 404)

    def patch(self):
        data = request.get_json()

        with self.session as session:
            task_service = TaskService(session)

            try:
                stmt = task_service.update_task(data)
                response = jsonify(stmt.model_dump(mode="json"))

                logger.info(
                    f"POST /v1/tasks : tarefa {response} atualizada com sucesso"
                )
                return make_response(202)

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

        return make_response(data, 200)

    def delete(self):
        # data = jsonify({"message": "Task deleted"})
        return make_response("", 204)
