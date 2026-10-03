from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

# Base configuration to reuse across read models
orm_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    name: str
    email: EmailStr  # Automatically validates email formatting
    password: str


class ReadUser(BaseModel):
    model_config = orm_config

    id: str
    name: str
    email: str
    created_at: datetime


class ReadMessage(BaseModel):
    model_config = orm_config

    id: str
    role: str
    content: str
    created_at: datetime


class ReadConversation(BaseModel):
    model_config = orm_config

    id: str
    title: str
    created_at: datetime
    messages: list[ReadMessage] = []


class ChatMessage(BaseModel):
    conversation_id: str | None = None
    content: str
