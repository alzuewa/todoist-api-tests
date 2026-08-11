import allure
import pytest
from allure_commons.types import Severity

import api.projects
from data.models.response_models import GetAllProjectsResponse, ProjectResponse
from data.project_constants import Color, ViewStyle


@allure.epic('Projects')
@allure.story('Get project')
@allure.title('[Project] Get. Existing project.')
@allure.description('Existing project should be accessible')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_get_one_project(session, create_new_project):
    new_project = create_new_project

    with allure.step(f'Get project with id: {new_project.id}'):
        resp = api.projects.get_project(session, project_id=new_project.id)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step('Validate field values'):
        assert project_response.name == new_project.name
        assert project_response.id == new_project.id
        assert project_response.parent_id is None
        assert project_response.color == Color.CHARCOAL
        assert project_response.is_shared is False
        assert project_response.is_favorite is False
        assert project_response.inbox_project is False
        assert project_response.view_style == ViewStyle.LIST


@allure.epic('Projects')
@allure.story('Get project')
@allure.title('[Project] Get. Full list of projects.')
@allure.description('List of all the projects should be accessible')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_get_all_projects(session, create_new_project):
    default_project_count = 1
    expected_projects = {'Inbox', create_new_project.name}

    with allure.step('Get all projects'):
        resp = api.projects.get_all_projects(session)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        projects_response = GetAllProjectsResponse.model_validate(resp.json())
        projects = projects_response.results

    with allure.step(f'Assert projects count is {default_project_count + 1}'):
        assert len(projects) == default_project_count + 1

    with allure.step(f'Assert projects\' names match expected values'):
        actual_projects = set([proj.name for proj in projects])
        assert actual_projects == expected_projects


@allure.epic('Authorization')
@allure.title('[Project][Unauthorized] Get.')
@allure.description('Project can not be retrieved with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_get_project__unauthorized(unauthorized_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make an unauthorized request'):
        resp = api.projects.get_project(unauthorized_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Project][Invalid token] Get.')
@allure.description('Project can not be retrieved with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_get_project__invalid_token(invalid_auth_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make a request with invalid token'):
        resp = api.projects.get_project(invalid_auth_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
