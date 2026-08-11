from typing import Literal, List

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from data.project_constants import Color, ViewStyle


class ProjectRequest(BaseModel):
    name: str | None = None
    parent_id: str | None = None
    color: Color | str | None = None
    is_favorite: bool | None = None
    view_style: ViewStyle | None = None


class Due(BaseModel):
    date: str
    is_recurring: bool
    datetime: str
    string: str
    timezone: str


class Duration(BaseModel):
    amount: int
    unit: Literal['minute', 'day']


class CreateTaskRequest(BaseModel):
    content: str
    description: str | None = None
    project_id: str | None = None
    section_id: str | None = None
    parent_id: str | None = None
    order: Annotated[int, Field(gt=0)] | None = None
    labels: List[str] | None = None
    priority: int | None = None
    assignee_id: str | None = None
    due_string: str | None = None
    due_date: str | None = None
    due_datetime: str | None = None
    due_lang: str | None = None
    duration: int | None = None
    duration_unit: Literal['minute', 'day'] | None = None
    deadline_date: str | None = None


class UpdateTaskRequest(BaseModel):
    content: str | None = None
    description: str | None = None
    project_id: str | None = None
    section_id: str | None = None
    parent_id: str | None = None
    order: Annotated[int, Field(gt=0)] | None = None
    labels: List[str] | None = None
    priority: int | None = None
    assignee_id: str | None = None
    due_string: str | None = None
    due_date: str | None = None
    due_datetime: str | None = None
    due_lang: str | None = None
    duration: int | None = None
    duration_unit: Literal['minute', 'day'] | None = None
    deadline_date: str | None = None
    child_order: int | None = None
    is_collapsed: bool | None = None
    day_order: int | None = None
