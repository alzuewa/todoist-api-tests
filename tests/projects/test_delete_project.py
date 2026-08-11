import allure
import pytest
from allure_commons.types import Severity

import api.projects


@allure.epic('Projects')
@allure.story('Delete project')
@allure.title('[Project] Delete. Existing project.')
@allure.description('After deletion project can not be accessed')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_delete_existing_project(session, create_new_project):
    new_project = create_new_project

    with allure.step(f'Delete project: {new_project.name}'):
        resp = api.projects.delete_project(session, project_id=new_project.id)
    with allure.step(f'Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step(f'Assert deleted project can not be retrieved and 404 response code is returned'):
        assert api.projects.get_project(session, project_id=new_project.id).status_code == 404


@allure.epic('Projects')
@allure.story('Delete project')
@allure.title('[Project] Delete. Not existing project.')
@allure.description('Deleting not existing project should result in getting error message')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.PROJECTS
def test_delete_not_existing_project(session):
    with allure.step(f'Delete not existing project'):
        resp = api.projects.delete_project(session, project_id='6XGgm6PHrGgMpBFX')
    with allure.step(f'Assert response code is 400'):
        assert resp.status_code == 400
        assert 'Value error, Invalid ProjectID' in resp.text


@allure.epic('Authorization')
@allure.title('[Project][Unauthorized] Delete.')
@allure.description('Project can not be deleted with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_delete_project__unauthorized(unauthorized_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make an unauthorized request'):
        resp = api.projects.delete_project(unauthorized_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Project][Invalid token] Delete.')
@allure.description('Project can not be deleted with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
@pytest.mark.PROJECTS
def test_delete_project__invalid_token(invalid_auth_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make a request with invalid token'):
        resp = api.projects.delete_project(invalid_auth_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
