from pydantic import BaseModel, validator #type: ignore
from datetime import datetime
from typing import Union

class Event(BaseModel):
    '''
    Validates the parameters given to trigger an event.
    Args:
        timestamp(datetime): the time of occurrence of requesting query.
        event(str): an event which user want to trigger.
    '''
    timestamp: str = ""
    event: str = ""
    
    @validator('timestamp')
    def must_be_a_timestamp(cls, v: str) -> Union[datetime, str]:
        try:
            s = datetime.fromtimestamp(float(v))
        except ValueError:
            return "Failure"
        return s

    @validator('event')
    def must_be_a_valid_event(cls, v: str) -> str:
        if v == None or v == "":
            return "Failure"
        return v

class Workflow(BaseModel):
    '''
    Validates the parameters given to trigger an event.
    Args:
        timestamp(datetime): the time of occurrence of requesting query.
        event(str): an event which user want to trigger.
        workflow(str): the workflow which user want to trigger.
    '''
    workflow: str = ""
    timestamp: str = ""
    event: str = ""
    
    @validator('workflow')
    def must_be_a_valid_workflow(cls, v: str) -> str:
        if v == None or v == "":
            return "Failure"
        return v

    @validator('timestamp')
    def must_be_a_timestamp(cls, v: str) -> Union[datetime, str]:
        try:
            s = datetime.fromtimestamp(float(v))
        except ValueError:
            return "Failure"
        return s

    @validator('event')
    def must_be_a_valid_event(cls, v: str) -> str:
        if v == None or v == "":
            return "Failure"
        return v
