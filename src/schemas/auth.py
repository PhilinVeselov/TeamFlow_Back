from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from typing import List, Optional

class TokenData(BaseModel):
    access_token: str
    refresh_token: str  
    token_type: str

class LoginSchema(BaseModel):
    username: str
    password: str

class RegisterParticipant(BaseModel):
    name: str
    email: EmailStr
    password: str
    description: Optional[str] = None
    img: Optional[str] = None
    technology_stack_ids: List[int] 


class RegisterOrganization(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_name: str
    organization_domain: str  # ← теперь обязательное поле
    organization_email: EmailStr
