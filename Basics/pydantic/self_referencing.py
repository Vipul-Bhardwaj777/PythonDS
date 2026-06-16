from pydantic import BaseModel
from typing import Optional, List

class Comments(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comments']] = None

Comments.model_rebuild()

comment = Comments(
    id=1,
    content='first comment',
    replies=[
        Comments(id=2, content='reply 1'),
        Comments(id=3, content='reply 2', replies=[Comments(id=4, content='nested reply')])
    ]
)