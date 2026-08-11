import allure
import pytest
from allure_commons.types import Severity

import api.projects
from data.models.request_models import ProjectRequest
from data.models.response_models import ProjectResponse
from data.project_constants import Color, ViewStyle


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field only.')
@allure.description('Project can be created with 1 required field: project name')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_create_project__only_required_param(session):
    with allure.step(f'Create the project with name: Shopping list'):
        new_project = ProjectRequest(name='Shopping list')
        resp = api.projects.create_project(session, json=new_project)

    with allure.step(f'Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert project_response.name == new_project.name
        assert project_response.color == Color.CHARCOAL
        assert project_response.is_shared is False
        assert project_response.is_favorite is False
        assert project_response.inbox_project is False
        assert project_response.view_style == ViewStyle.LIST
        assert project_response.parent_id is None


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. All the fields.')
@allure.description('Project can be created with several fields at once')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
@pytest.mark.PROJECTS
def test_create_project__all_params(session, create_new_project):
    parent_project = create_new_project

    with allure.step(f'Create the project with all the params filled'):
        child_project = ProjectRequest(
            name='Shopping list inner',
            parent_id=parent_project.id,
            color=Color.YELLOW,
            is_favorite=True,
            view_style=ViewStyle.LIST
        )
        resp = api.projects.create_project(session, json=child_project)

    with allure.step(f'Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert project_response.name == child_project.name
        assert project_response.color == Color.YELLOW
        assert project_response.is_shared is False
        assert project_response.is_favorite is True
        assert project_response.inbox_project is False
        assert project_response.view_style == ViewStyle.LIST
        assert project_response.parent_id == parent_project.id


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field missed.')
@allure.description('Project can not be created without required field')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_create_project__required_param_missed(session):
    with allure.step(f'Create project without body in request'):
        resp = api.projects.create_project(session)
    with allure.step(f'Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert 'Required argument is missing' in resp.text


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field invalid value.')
@allure.description('Project can not be created with invalid required field values: "", " "')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize('name', ['', pytest.param(' ', marks=[pytest.mark.skip(reason='Issue #12345')])])
@pytest.mark.PROJECTS
def test_create_project__required_param_invalid_value(session, name):
    with allure.step(f'Create project with invalid name: "{name}"'):
        new_project = ProjectRequest(name=name)
        resp = api.projects.create_project(session, json=new_project)
    with allure.step(f'Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert 'Name must be provided for the project creation' in resp.text


@allure.epic('Authorization')
@allure.title('[Project][Unauthorized] Create.')
@allure.description('Project can not be created with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_create_project__unauthorized(unauthorized_session):
    with allure.step('Make an unauthorized request'):
        new_project = ProjectRequest(name='Test Project')
        resp = api.projects.create_project(unauthorized_session, json=new_project)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Project][Invalid token] Create.')
@allure.description('Project can not be created with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_create_project__invalid_token(invalid_auth_session):
    with allure.step('Make a request with invalid token'):
        new_project = ProjectRequest(name='Test Project')
        resp = api.projects.create_project(invalid_auth_session, json=new_project)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
