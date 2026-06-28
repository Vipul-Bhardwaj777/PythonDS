from pydantic import BaseModel, Field
from typing import Optional
import re


class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee name",
        example="Vipul Bhardwaj",
    )
    salary: float = Field(..., ge=0, le=100000)
    department: Optional[str] = "general"
