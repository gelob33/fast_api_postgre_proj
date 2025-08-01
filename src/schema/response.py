from pydantic import BaseModel
from uuid import UUID

#----------------------------------------- # 
# Response shapes you send back to clients #
#----------------------------------------- # 
class Book(BaseModel):
    id: UUID
    title: str
    author: str
    category: str
