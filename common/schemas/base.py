from datetime import datetime
from pydantic import BaseModel as BaseModelPydantic


class BaseModel(BaseModelPydantic):
    id: int
    modified: datetime
    created_time: datetime