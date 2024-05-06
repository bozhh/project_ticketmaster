from pydantic import BaseModel

class EventDescription(BaseModel):
    event_id: int
    description: str

class EventReview(BaseModel):
    event_id: str
    review: int
    text: str
    user: str
    user_id: int