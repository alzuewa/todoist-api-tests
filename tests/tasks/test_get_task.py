import allure
import pytest
from allure_commons.types import Severity

import api.tasks
from data.models.request_models import CreateTaskRequest
from data.models.response_models import GetTaskResponse, GetAllTasksResponse


@allure.epic('Tasks')
@allure.story('Get task')
@allure.title('[Task] Get. Existing task.')
@allure.description('Existing task can be retrieved')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_get_one_task(session, create_new_task):
    new_task = create_new_task

    with allure.step(f'Get task: id={new_task.id}'):
        resp = api.tasks.get_task(session, task_id=new_task.id)

    with allure.step(f'Validate json response schema'):
        task_response = GetTaskResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert task_response.content == new_task.content
        assert task_response.checked == new_task.checked
        assert task_response.description == new_task.description
        assert task_response.labels == new_task.labels
        assert task_response.priority == new_task.priority
        assert task_response.project_id == new_task.project_id
        assert task_response.section_id == new_task.section_id


@allure.epic('Tasks')
@allure.story('Get task')
@allure.title('[Task] Get. Full list of active tasks.')
@allure.description('List of all the active tasks should be accessible')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_get_all_tasks(session, create_new_task):
    new_task_1 = create_new_task

    with allure.step('Create task: Call the friend'):
        new_task_2 = CreateTaskRequest(content='Call the friend')
        api.tasks.create_task(session, json=new_task_2)
        expected_tasks = {new_task_1.content, new_task_2.content}

    with allure.step('Get all tasks'):
        resp = api.tasks.get_all_tasks(session)

    with allure.step(f'Validate json response schema'):
        tasks_response = GetAllTasksResponse.model_validate(resp.json())

    with allure.step(f'Assert tasks count is 2'):
        assert len(tasks_response.results) == 2

    with allure.step(f'Assert tasks\' content match expected values'):
        actual_tasks = set([task.content for task in tasks_response.results])
        assert actual_tasks == expected_tasks


@allure.epic('Authorization')
@allure.title('[Task][Unauthorized] Get.')
@allure.description('Task can not be retrieved with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
@pytest.mark.skip(reason='Issue #875: Unauthorized request returns 404')
def test_get_task__unauthorized(unauthorized_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make an unauthorized request'):
        resp = api.tasks.get_task(unauthorized_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Task][Invalid token] Get.')
@allure.description('Task can not be retrieved with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.TASKS
def test_get_task__invalid_token(invalid_auth_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make a request with invalid token'):
        resp = api.tasks.get_task(invalid_auth_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
