import re

import allure
import pytest
from allure_commons.types import Severity

import api.projects
from data.models.request_models import ProjectRequest
from data.models.response_models import ProjectResponse
from data.project_constants import Color, ViewStyle


@allure.epic('Projects')
@allure.story('Update project')
@allure.title('[Project] Update. Existing project.')
@allure.description('Project fields can be updated')
@allure.tag('Edit')
@allure.severity(Severity.NORMAL)
@pytest.mark.PROJECTS
def test_update__all_params(session, create_new_project):
    new_project = create_new_project

    with allure.step('Update project fields'):
        updated_fields = ProjectRequest(name='Travelling', color=Color.LIME_GREEN, is_favorite=True,
                                        view_style=ViewStyle.BOARD)
        resp = api.projects.update_project(session, project_id=new_project.id, json=updated_fields)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step('Validate field values'):
        assert project_response.name == updated_fields.name
        assert project_response.color == updated_fields.color
        assert project_response.is_shared is False
        assert project_response.is_favorite == updated_fields.is_favorite
        assert project_response.inbox_project is False
        assert project_response.view_style == updated_fields.view_style
        assert project_response.parent_id is None


@allure.epic('Projects')
@allure.story('Update project')
@allure.title('[Project] Update. Empty request.')
@allure.description('At least 1 field should be passed to update the project')
@allure.tag('Edit')
@allure.severity(Severity.NORMAL)
@pytest.mark.PROJECTS
def test_update_without_params(session, create_new_project):
    new_project = create_new_project

    with allure.step('Send update project request without body'):
        resp = api.projects.update_project(session, project_id=new_project.id)

    with allure.step('Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert re.search(r'At least one of.*fields should be set', resp.text)


@allure.epic('Projects')
@allure.story('Update project')
@allure.title('[Project] Update. Available color.')
@allure.description('Project color can be updated within a specific range of colors')
@allure.tag('Edit')
@allure.severity(Severity.NORMAL)
@pytest.mark.PROJECTS
@pytest.mark.parametrize('color', [color for color in Color if color != Color.CHARCOAL])
def test_update__valid_color(session, create_new_project, color):
    new_project = create_new_project

    with allure.step(f'Update project color with valid value: {color}'):
        updated_fields = ProjectRequest(color=color)
        resp = api.projects.update_project(session, project_id=new_project.id, json=updated_fields)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step('Validate the project color has been updated'):
        assert project_response.id == new_project.id
        assert project_response.color == updated_fields.color


@allure.epic('Projects')
@allure.story('Update project')
@allure.title('[Project] Update. Unavailable color.')
@allure.description('Project color can not be updated with unavailable color')
@allure.tag('Edit')
@allure.severity(Severity.MINOR)
@pytest.mark.PROJECTS
def test_update__invalid_color(session, create_new_project):
    new_project = create_new_project

    with allure.step(f'Update project color with invalid value: white'):
        updated_fields = ProjectRequest(color='white')
        resp = api.projects.update_project(session, project_id=new_project.id, json=updated_fields)
    with allure.step('Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert 'Invalid argument value' in resp.text


@allure.epic('Authorization')
@allure.title('[Project][Unauthorized] Update.')
@allure.description('Project can not be updated with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_update_project__unauthorized(unauthorized_session, create_new_project):
    new_project = create_new_project
    json = ProjectRequest(is_favorite=True)
    with allure.step('Make an unauthorized request'):
        resp = api.projects.update_project(unauthorized_session, project_id=new_project.id, json=json)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Project][Invalid token] Update.')
@allure.description('Project can not be updated with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_update_project__invalid_token(invalid_auth_session, create_new_project):
    new_project = create_new_project
    json = ProjectRequest(is_favorite=True)
    with allure.step('Make a request with invalid token'):
        resp = api.projects.update_project(invalid_auth_session, project_id=new_project.id, json=json)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
