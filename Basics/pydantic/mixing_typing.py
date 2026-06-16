from pydantic import BaseModel
from typing import List, Dict, Optional

class Cart(BaseModel):
    user_id: int
    items: List[str]
    quantity: Dict[str, int]
    price: float
    slug: Optional[str] = None