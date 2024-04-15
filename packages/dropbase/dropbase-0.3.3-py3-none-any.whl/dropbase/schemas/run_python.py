from typing import Any, Dict, Optional

from pydantic import BaseModel

from dropbase.schemas.table import FilterSort


class QueryTablePayload(BaseModel):
    context: Dict[str, Any]
    state: Dict[str, Any]


class RunPythonStringRequest(BaseModel):
    app_name: str
    page_name: str
    python_string: str
    payload: QueryTablePayload
    file: dict


class RunPythonStringRequestNew(BaseModel):
    file_code: str
    test_code: str
    state: dict
    context: dict


class QueryPythonRequest(BaseModel):
    app_name: str
    page_name: str
    fetcher: str
    filter_sort: Optional[FilterSort]
    state: dict
