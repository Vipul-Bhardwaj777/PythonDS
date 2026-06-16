from pydantic import BaseModel, computed_field, Field

class Booking(BaseModel):
    user_id: int
    room_id: int
    nights: int = Field(..., ge=1)
    rate_per_night: float = Field(..., ge=100)

    @computed_field
    @property
    def total_bill(self) -> float:
        return self.nights * self.rate_per_night
    
booking1 = Booking(
    user_id = 232, 
    room_id = 867, 
    nights = 3,
    rate_per_night = 300
)

print(booking1.model_dump())