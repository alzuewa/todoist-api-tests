import allure
import pytest
from allure_commons.types import Severity

import api.tasks
from data.models.request_models import UpdateTaskRequest
from data.models.response_models import UpdateTaskResponse


@allure.epic('Tasks')
@allure.story('Update task')
@allure.title('[Task] Update. Description.')
@allure.description('Task description can be updated')
@allure.tag('Edit', 'New feature')
@allure.severity(Severity.NORMAL)
@pytest.mark.TASKS
def test_update_task_description(session, create_new_task):
    new_task = create_new_task
    with allure.step('Update task description'):
        updated_fields = UpdateTaskRequest(description='1 loaf')
        resp = api.tasks.update_task(session, task_id=new_task.id, json=updated_fields)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        task_response = UpdateTaskResponse.model_validate(resp.json())

    with allure.step('Validate the task description has been updated'):
        assert task_response.id == new_task.id
        assert task_response.description == updated_fields.description


@allure.epic('Tasks')
@allure.story('Update task')
@allure.title('[Task] Update. Priority. Invalid values.')
@allure.description('Task priority can be updated within a specific range of numbers')
@allure.tag('Edit', 'New feature')
@allure.severity(Severity.NORMAL)
@pytest.mark.TASKS
@pytest.mark.parametrize('priority', [-1, 0, 5])
def test_update_task__invalid_priority(session, create_new_task, priority):
    new_task = create_new_task

    with allure.step(f'Update task priority with invalid value: {priority=}'):
        updated_fields = UpdateTaskRequest(priority=priority)
        resp = api.tasks.update_task(session, task_id=new_task.id, json=updated_fields)

    with allure.step('Validate response json schema'):
        task_response = UpdateTaskResponse.model_validate(resp.json())

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Assert task priority value has not changed'):
        assert task_response.priority == new_task.priority


@allure.epic('Authorization')
@allure.title('[Task][Unauthorized] Update.')
@allure.description('Task can not be updated with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_update_task__unauthorized(unauthorized_session, create_new_task):
    new_task = create_new_task
    json = UpdateTaskRequest(priority=2)
    with allure.step('Make an unauthorized request'):
        resp = api.tasks.update_task(unauthorized_session, task_id=new_task.id, json=json)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Task][Invalid token] Update.')
@allure.description('Task can not be updated with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_update_task__invalid_token(invalid_auth_session, create_new_task):
    new_task = create_new_task
    json = UpdateTaskRequest(priority=2)
    with allure.step('Make a request with invalid token'):
        resp = api.tasks.update_task(invalid_auth_session, task_id=new_task.id, json=json)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
