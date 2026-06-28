from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator


class User(BaseModel):
    name: str
    last_name: str
    email: str
    earning: float  # 4.44
    start_date: datetime
    end_date: datetime

    @field_validator("name", "last_name")
    def validate_names(cls, v):
        if not v.istitle():
            raise ValueError("Names should be capitalized")
        return v

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower().strip()

    @field_validator("earning", mode="before")
    def parse_price(cls, v):
        if isinstance(v, str):
            return float(v.replace("$", "").replace(",", ""))
        return v

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date cannot be after end date")
        return self
