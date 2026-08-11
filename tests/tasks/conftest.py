import allure
import pytest

import api.tasks
from data.models.request_models import CreateTaskRequest
from data.models.response_models import GetAllTasksResponse, CreateTaskResponse


@pytest.fixture(scope='function')
def create_new_task(session):
    with allure.step(f'Create fixture task with name: Buy bread'):
        task = CreateTaskRequest(content='Buy bread')
        resp = api.tasks.create_task(session, task)
        task_resp = CreateTaskResponse.model_validate(resp.json())
        return task_resp


@pytest.fixture(scope='function', autouse=True)
def delete_all_tasks(session):
    yield

    with allure.step(f'Delete all tasks'):
        api_response = api.tasks.get_all_tasks(session).json()
        response_model = GetAllTasksResponse.model_validate(api_response)
        task_ids = [task.id for task in response_model.results]
        for task_id in task_ids:
            api.tasks.delete_task(session, task_id=task_id)
