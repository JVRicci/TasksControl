import logging

from flask import Blueprint, request, jsonify, make_response
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
        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("", methods=["PATCH"])
def update_task():
    data = request.get_json()

    try:
        with SessionLocal() as session:
            task_service = TaskService(session)
            task = task_service.update_task(data)

            return make_response(
                jsonify(task.model_dump(mode="json")),
                200,
            )

    except ValidationError as exc:
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
        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    with SessionLocal() as session:
        task_service = TaskService(session)
        task_service.delete_task(task_id)

    return make_response("", 204)
