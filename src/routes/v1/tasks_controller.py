import logging

from flask import Blueprint, jsonify, make_response, request
from pydantic import ValidationError

from src.db.database import SessionLocal
from src.services.task_services import TaskService
from src.schemas.task_query_schema import TaskQuerySchema

logger = logging.getLogger(__name__)

api_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@api_bp.route("", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    try:
        with SessionLocal() as session:
            task_service = TaskService(session)
            task = task_service.create_task(data)

            return make_response(
                jsonify(task.model_dump(mode="json")),
                201,
            )

    except ValidationError as exc:
        logger.warning(
            "POST /v1/tasks rejected: Erro ao cadastrar tarefa. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify(
                {
                    "error": "Dados inválidos",
                    "details": exc.errors(include_url=False),
                }
            ),
            400,
        )

    except ValueError as exc:
        logger.warning(
            "POST /v1/tasks rejected: Erro ao cadastrar tarefa. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("", methods=["GET"])
def get_tasks():
    try:
        query = TaskQuerySchema.model_validate(request.args.to_dict())

        with SessionLocal() as session:
            task_service = TaskService(session)

            if query.completed is None:
                tasks = task_service.get_by_user(query.user_id)
            else:
                tasks = task_service.get_by_status(
                    query.user_id,
                    query.completed,
                )

            response = [task.model_dump(mode="json") for task in tasks]

            return make_response(jsonify(response), 200)

    except ValidationError as exc:
        logger.warning(
            "GET /v1/tasks rejected: Erro ao validar tarefa. \nDetalhes: {exc}"
        )

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
        logger.warning(
            "GET /v1/tasks rejected: Erro ao cadastrar tarefa. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id: int):
    try:
        with SessionLocal() as session:
            task_service = TaskService(session)
            task = task_service.get_task_by_id(task_id)

            return make_response(
                jsonify(task.model_dump(mode="json")),
                200,
            )

    except ValueError as exc:
        logger.warning(
            "GET /v1/tasks rejected: Erro ao buscar tarefa. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("", methods=["PATCH"])
def update_task():
    data = request.get_json(silent=True)

    try:
        with SessionLocal() as session:
            task_service = TaskService(session)
            task = task_service.update_task(data)

            return make_response(
                jsonify(task.model_dump(mode="json")),
                200,
            )

    except ValidationError as exc:
        logger.warning(
            "PATCH /v1/tasks rejected: Erro ao atualizar tarefa. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify(
                {
                    "error": "Dados inválidos",
                    "details": exc.errors(include_url=False),
                }
            ),
            400,
        )

    except ValueError as exc:
        logger.warning(
            "POST /v1/tasks rejected: Erro ao atualizar tarefa. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    try:
        with SessionLocal() as session:
            task_service = TaskService(session)
            task_service.delete_task(task_id)

        return make_response("", 204)
    except ValidationError as exc:
        logger.warning(
            f"DELETE /v1/tasks/{task_id} rejected: tarefa inválido ou inexistente. \nDetalhes: {exc}"
        )
        return make_response(jsonify("Tarefa inválida"), 400)
