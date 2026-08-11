from typing import Optional

from data.models.request_models import CreateTaskRequest
from utils.session import ApiSession


def create_task(session: ApiSession, json: Optional[CreateTaskRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post('/tasks', json=json)
    else:
        with session:
            response = session.post('/tasks')
    return response


def get_all_tasks(session: ApiSession):
    with session:
        response = session.get('/tasks')
    return response


def get_task(session: ApiSession, task_id: str):
    with session:
        response = session.get(f'/tasks/{task_id}')
    return response


def delete_task(session: ApiSession, task_id: str):
    with session:
        response = session.delete(f'/tasks/{task_id}')
    return response


def update_task(session: ApiSession, task_id: str, json: Optional[CreateTaskRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post(f'/tasks/{task_id}', json=json)
    else:
        with session:
            response = session.post(f'/tasks/{task_id}')
    return response


def close_task(session: ApiSession, task_id: str):
    with session:
        response = session.post(f'/tasks/{task_id}/close')
    return response


def reopen_task(session: ApiSession, task_id: str):
    with session:
        response = session.post(f'/tasks/{task_id}/reopen')
    return response
