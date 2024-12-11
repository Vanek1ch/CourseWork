import uuid

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import Field as Pfield

class Role(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    
        
class Users(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    role_id: int = Field(foreign_key='role.id')
    role: Role = Relationship()
    nickname: str = Field(unique=True)
    password: str
    created_at: datetime