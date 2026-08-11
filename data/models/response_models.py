from typing import List

import pydantic
from pydantic import BaseModel, TypeAdapter
from typing_extensions import Annotated, deprecated
from data.models.request_models import Due, Duration
from data.project_constants import Color, ViewStyle


class ProjectResponse(BaseModel):
    id: str
    name: str
    color: Color
    is_shared: bool
    is_favorite: bool
    parent_id: str | None
    inbox_project: bool
    view_style: ViewStyle


@deprecated('Use "GetAllProjectsResponse" instead')
class AllProjectsResponse:

    @staticmethod
    def model_validate(response):
        all_projects_response = TypeAdapter(List[ProjectResponse])
        return all_projects_response.validate_python(response)


class GetAllProjectsResponse(BaseModel):
    results: list[ProjectResponse]
    next_cursor: str | None


class CreateTaskResponse(BaseModel):
    user_id: str
    id: str
    project_id: str
    section_id: str | None = None
    parent_id: str | None = None
    added_by_uid: str
    assigned_by_uid: str | None = None
    responsible_uid: str | None = None
    labels: List[str]
    deadline: str | None
    duration: Duration | None = None
    is_collapsed: bool
    checked: bool
    is_deleted: bool
    added_at: str
    completed_at: str | None
    completed_by_uid: str | None
    updated_at: str | None
    due: Due | None = None
    priority: Annotated[int, pydantic.Field(ge=1), pydantic.Field(le=4)]
    child_order: int
    content: str
    description: str
    note_count: int
    day_order: int
    completed_count: int
    postponed_count: int


class GetTaskResponse(BaseModel):
    user_id: str
    id: str
    project_id: str
    section_id: str | None = None
    parent_id: str | None = None
    added_by_uid: str
    assigned_by_uid: str | None = None
    responsible_uid: str | None = None
    labels: List[str]
    deadline: str | None
    duration: Duration | None = None
    is_collapsed: bool
    checked: bool
    is_deleted: bool
    added_at: str
    completed_at: str | None
    completed_by_uid: str | None
    updated_at: str | None
    due: Due | None = None
    priority: Annotated[int, pydantic.Field(ge=1), pydantic.Field(le=4)]
    child_order: int
    content: str
    description: str
    note_count: int
    day_order: int
    completed_count: int
    postponed_count: int


class UpdateTaskResponse(BaseModel):
    user_id: str
    id: str
    project_id: str
    section_id: str | None = None
    parent_id: str | None = None
    added_by_uid: str
    assigned_by_uid: str | None = None
    responsible_uid: str | None = None
    labels: List[str]
    deadline: str | None
    duration: Duration | None = None
    is_collapsed: bool
    checked: bool
    is_deleted: bool
    added_at: str
    completed_at: str | None
    completed_by_uid: str | None
    updated_at: str | None
    due: Due | None = None
    priority: Annotated[int, pydantic.Field(ge=1), pydantic.Field(le=4)]
    child_order: int
    content: str
    description: str
    note_count: int
    day_order: int
    completed_count: int
    postponed_count: int


@deprecated('Use "GetAllTasksResponse" instead')
class AllTasksResponse:

    @staticmethod
    def model_validate(response):
        all_tasks_response = TypeAdapter(List[GetTaskResponse])
        return all_tasks_response.validate_python(response)


class GetAllTasksResponse(BaseModel):
    results: list[GetTaskResponse]
    next_cursor: str | None