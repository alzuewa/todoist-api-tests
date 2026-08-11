import secrets

import allure
import pytest

import api.projects
from config.test_project_config import config
from data.models.request_models import ProjectRequest
from data.models.response_models import ProjectResponse
from utils.session import ApiSession, BearerAuth


@pytest.fixture(scope='package', name='session')
def authorized_session():
    session = ApiSession(base_url=test_config.base_url, auth=BearerAuth(test_config.token))

    yield session


@pytest.fixture(scope='function')
def unauthorized_session():
    session = ApiSession(base_url=test_config.base_url)

    yield session


@pytest.fixture(scope='function')
def invalid_auth_session():
    random_token = secrets.token_hex(20)
    session = ApiSession(base_url=config.base_url, auth=BearerAuth(random_token))

    yield session


@pytest.fixture(scope='function', autouse=True)
def delete_all_created_projects(session):
    yield

    with allure.step(f'Delete all created projects but Inbox'):
        api.projects.delete_all_projects_but_inbox(session)


@pytest.fixture(scope='function')
def create_new_project(session):
    with allure.step(f'Create fixture project with name: Shopping list'):
        project = ProjectRequest(name='Shopping list')
        resp = api.projects.create_project(session, project)
        project_resp = ProjectResponse.model_validate(resp.json())
        return project_resp
