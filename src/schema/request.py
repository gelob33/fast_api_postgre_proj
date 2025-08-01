from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID

#----------------------------- # 
# Request payloads from client #
#----------------------------- # 
class CreateBook(BaseModel):
    title: str = Field(..., description="The title of the Book")
    author: str = Field(..., description="Name of the book author")
    category: Optional[str] = Field(..., description="Book category") 

    @field_validator('title', 'author')
    @classmethod
    def must_not_be_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Field must not be blank or whitespaces")
        return v