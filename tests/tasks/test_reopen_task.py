import allure
import pytest
from allure_commons.types import Severity

import api.tasks
from data.models.request_models import CreateTaskRequest
from data.models.response_models import GetTaskResponse, GetAllTasksResponse


@allure.epic('Tasks')
@allure.story('Reopen task')
@allure.title('[Task] Reopen. Single existing task.')
@allure.description('Existing closed task can be reopened')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.TASKS
def test_reopen_existing_task(session, create_new_task):
    new_task = create_new_task
    with allure.step(f'Close task: id={new_task.id}, content={new_task.content}'):
        api.tasks.close_task(session, task_id=new_task.id)
    with allure.step('Reopen previously closed task'):
        resp = api.tasks.reopen_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert reopened task is now in all active tasks list'):
        all_active_tasks_api = api.tasks.get_all_tasks(session).json()
        all_active_tasks = GetAllTasksResponse.model_validate(all_active_tasks_api)
        assert new_task.id in [task.id for task in all_active_tasks.results]


@allure.epic('Tasks')
@allure.story('Reopen task')
@allure.title('[Task] Reopen. Task with an ancestor.')
@allure.description('Task reopening also reopens its ancestor')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.TASKS
def test_reopen_task_with_ancestor(session, create_new_task):
    ancestor_task = create_new_task
    with allure.step(f'Create child task: Withdraw cash'):
        child_task = CreateTaskRequest(content='Withdraw cash', parent_id=ancestor_task.id)
        resp = api.tasks.create_task(session, json=child_task)
        child_task_response = GetTaskResponse.model_validate(resp.json())

    with allure.step(f'Close child task: id={child_task_response.id}, content={child_task_response.content}'):
        api.tasks.close_task(session, task_id=child_task_response.id)
    with allure.step(f'Close ancestor task: id={ancestor_task.id}, content={ancestor_task.content}'):
        api.tasks.close_task(session, task_id=ancestor_task.id)

    with allure.step('Assert closed ancestor and child tasks are not in all active tasks list'):
        all_active_tasks_api = api.tasks.get_all_tasks(session).json()
        all_active_tasks = GetAllTasksResponse.model_validate(all_active_tasks_api)
        active_task_ids = [task.id for task in all_active_tasks.results]
        assert ancestor_task.id not in active_task_ids
        assert child_task_response.id not in active_task_ids

    with allure.step('Reopen previously closed child task'):
        resp = api.tasks.reopen_task(session, task_id=child_task_response.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204

    with allure.step('Assert reopened child task is now in all active tasks list'):
        all_active_tasks_api = api.tasks.get_all_tasks(session).json()
        all_active_tasks = GetAllTasksResponse.model_validate(all_active_tasks_api)
        active_task_ids = [task.id for task in all_active_tasks.results]
        assert child_task_response.id in active_task_ids
        assert ancestor_task.id in active_task_ids


@allure.epic('Tasks')
@allure.story('Reopen task')
@allure.title('[Task] Reopen. Not closed task.')
@allure.description('Reopening not closed task is correctly handled')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.TASKS
def test_reopen_not_closed_task(session, create_new_task):
    new_task = create_new_task
    with allure.step('Reopen not closed task'):
        resp = api.tasks.reopen_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert reopened task is still in all active tasks list'):
        all_active_tasks_api = api.tasks.get_all_tasks(session).json()
        all_active_tasks = GetAllTasksResponse.model_validate(all_active_tasks_api)
        assert new_task.id in [task.id for task in all_active_tasks.results]


@allure.epic('Authorization')
@allure.title('[Task][Unauthorized] Reopen.')
@allure.description('Task can not be reopened with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_reopen_task__unauthorized(session, unauthorized_session, create_new_task):
    new_task = create_new_task
    with allure.step('Close task with valid authorization'):
        api.tasks.close_task(session, task_id=new_task.id)
    with allure.step('Make an unauthorized request'):
        resp = api.tasks.reopen_task(unauthorized_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Task][Invalid token] Reopen.')
@allure.description('Task can not be reopened with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_reopen_task__invalid_token(session, invalid_auth_session, create_new_task):
    new_task = create_new_task
    with allure.step('Close task with valid authorization'):
        api.tasks.close_task(session, task_id=new_task.id)
    with allure.step('Make a request with invalid token'):
        resp = api.tasks.reopen_task(invalid_auth_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
