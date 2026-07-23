from pydantic import BaseModel

# 1. Define the data structure using a Pydantic model
class PasswordItem(BaseModel):
    key: str
    username: str
    password: str
    description: str | None = None
