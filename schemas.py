import datetime as _dt
import pydantic as _pydantic
from typing import List
from mongoModels import EventDescription, EventReview

class _BaseEvent(_pydantic.BaseModel):
    name: str
    date: _dt.date
    time: _dt.time
    venue: str
    available_tickets: int

    class Config:
        from_attributes = True

class Event(_BaseEvent):
    id: int

class CreateEvent(_BaseEvent):
    pass

class _BaseUser(_pydantic.BaseModel):
    name: str
    surname: str

    class Config:
        from_attributes = True

class Attender(_BaseUser):
    id: int

class Performer(_BaseUser):
    id: int

class CreateUser(_BaseUser):
    pass


class _BaseTicket(_pydantic.BaseModel):
    price: float
    type: str
    status: str
    seat_no: int

    class Config:
        from_attributes = True

class Ticket(_BaseTicket):
    id: int
    reservation_time: _dt.time
    owner: Attender

class TicketWithEvent(Ticket):
    event: Event

class CreateTicket(_BaseTicket):
    event_id: int

class PerformerWithEvent(Performer):
    events: List[Event] = []

class AttenderWithTickets(Attender):
    tickets: List[TicketWithEvent] = []

class EventWithTickets(Event):
    tickets: List[Ticket] = []
    performers: List[Performer] = []

class EventWithReviews(EventWithTickets):
    description: EventDescription
    reviews: List[EventReview] = []

