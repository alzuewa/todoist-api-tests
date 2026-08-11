from typing import Optional

from data.models.request_models import ProjectRequest
from data.models.response_models import GetAllProjectsResponse
from utils.session import ApiSession


def create_project(session: ApiSession, json: Optional[ProjectRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post('/projects', json=json)
    else:
        with session:
            response = session.post('/projects')
    return response


def get_project(session: ApiSession, project_id: str):
    with session:
        response = session.get(f'/projects/{project_id}')
    return response


def get_all_projects(session: ApiSession):
    with session:
        response = session.get('/projects')
    return response


def update_project(session: ApiSession, project_id: str, json: Optional[ProjectRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post(f'/projects/{project_id}', json=json)
    else:
        with session:
            response = session.post(f'/projects/{project_id}')
    return response


def delete_project(session: ApiSession, project_id: str):
    with session:
        response = session.delete(f'/projects/{project_id}')
    return response

def delete_all_projects_but_inbox(session: ApiSession):
    with session:
        api_response = get_all_projects(session)
        response_model = GetAllProjectsResponse.model_validate(api_response.json())
        project_ids = [project.id for project in response_model.results if project.name != 'Inbox']
        for project_id in project_ids:
            delete_project(session, project_id=project_id)
