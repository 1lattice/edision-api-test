from pydantic import BaseModel

class SwaggerApiDataCreate(BaseModel):
    api: str
    method_name: str
    platform: str
    priority: int
    group_name: str

class InputDataCreate(BaseModel):
    data: str
    swagger_api_id: int

class GroupNameCreate(BaseModel):
    group_name: str
    swagger_api_id: int

class ResultsCreate(BaseModel):
    status_code: int
    response_data: str
    error_message: str
    status: str
    swagger_api_id: int
