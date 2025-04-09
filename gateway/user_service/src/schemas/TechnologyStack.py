from pydantic import BaseModel

class TechnologyStackCreate(BaseModel):
    name: str

class TechnologyStackOut(BaseModel):
    id_technology_stack: int
    name: str

    class Config:
        from_attributes = True  # для Pydantic v2
