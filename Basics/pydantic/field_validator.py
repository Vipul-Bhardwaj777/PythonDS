from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    name: str

    @field_validator('name')
    def user_name_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Name cannot be less than 3 characters.')
        return v
    
class SignupData(BaseModel):
    password: str
    confirm_password: str

# Depricated
    @model_validator(mode='after')
    def vaid_pass(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Password did not match')
        return values
    
    @model_validator(mode='after')
    def valid2(self):
        if self.password != self.confirm_password:
            raise ValueError('Password did not match 2')
        return self
