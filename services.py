from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas
import datetime as _dt
import sqlalchemy.orm as _orm
import asyncio

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def auto_cancel_reservations(ticket_id: int, event_id: int, db: "Session"):
    await asyncio.sleep(15*60)
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    event = db.query(_models.Event).filter(_models.Event.id == event_id).first()
    if ticket.status == 'reserved':
        ticket.owner_id = None
        ticket.reservation_time = None
        ticket.status = 'available'
        event.available_tickets += 1
        db.commit()
        db.refresh(event)
        db.refresh(ticket)


# EVENTS
async def create_event(event: _schemas.CreateEvent, db:"Session") -> _schemas.Event:
    event = _models.Event(**event.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return _schemas.Event.from_orm(event)

async def get_all_events(db: "Session") -> List[_schemas.EventWithTickets]:
    events = db.query(_models.Event).all()
    return list(map(_schemas.EventWithTickets.from_orm, events))

async def get_event(event_id: int, db: "Session") -> _schemas.EventWithTickets:
    event = db.query(_models.Event).filter(_models.Event.id == event_id).first()
    return event

async def delete_event(event: _models.Event, db: "Session"):
    db.delete(event)
    db.commit()

async def update_event(event_data: _schemas.CreateEvent, event: _models.Event, db: "Session") -> _schemas.EventWithTickets:
    event.name = event_data.name
    event.date = event_data.date
    event.time = event_data.time
    event.venue = event_data.venue

    db.commit()
    db.refresh(event)

    return _schemas.EventWithTickets.from_orm(event)

async def get_2_months_ahead_events(date: _dt.date, db: "Session") -> List[_schemas.EventWithTickets]:
    two_months_ahead = date + _dt.timedelta(days=60)
    events = db.query(_models.Event).filter(date <= _models.Event.date, _models.Event.date <= two_months_ahead).all()
    return events


# TICKETS
async def create_ticket(ticket: _schemas.Ticket, db:"Session") -> _schemas.Ticket:
    ticket = _models.Ticket(**ticket.dict())
    event = db.query(_models.Event).filter(_models.Event.id == ticket.event_id).first()
    event.available_tickets += 1
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.refresh(event)
    return _schemas.Ticket.from_orm(ticket)

async def get_all_tickets(db: "Session") -> List[_schemas.TicketWithEvent]:
    tickets = db.query(_models.Ticket).all()
    return list(map(_schemas.TicketWithEvent.from_orm, tickets))

async def get_attender_tickets(attender_id: int, db: "Session") -> List[_schemas.TicketWithEvent]:
    tickets = db.query(_models.Ticket).filter(_models.Ticket.owner_id == attender_id).first()
    return tickets

async def get_ticket(ticket_id: int, db: "Session") -> _schemas.TicketWithEvent:
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    return ticket

async def delete_ticket(ticket: _models.Ticket, db: "Session"):
    event_id = ticket.event_id
    db.delete(ticket)
    db.commit()
    event = db.query(_models.Event).filter(_models.Event.id == event_id).first()
    event.available_tickets -= 1
    db.refresh(event)

async def update_ticket(ticket_data: _schemas.CreateTicket, ticket: _models.Ticket, db: "Session") -> _schemas.TicketWithEvent:
    ticket.price = ticket_data.price
    ticket.type = ticket_data.type
    ticket.status = ticket_data.status
    ticket.seat_no = ticket_data.seat_no

    db.commit()
    db.refresh(ticket)

    return _schemas.TicketWithEvent.from_orm(ticket)

async def buy_ticket(attender_id: int, ticket_id: int, db: "Session") -> _schemas.TicketWithEvent:
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    ticket.owner_id = attender_id
    ticket.status = "sold"
    ticket.reservation_time = None
    event = db.query(_models.Event).filter(_models.Event.id == ticket.event_id).first()
    event.available_tickets -= 1
    db.commit()
    db.refresh(ticket)
    db.refresh(event)
    return _schemas.TicketWithEvent.from_orm(ticket)

async def return_ticket(ticket_id: int, attender_id: int, db: "Session") -> _schemas.TicketWithEvent:
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    ticket.owner_id = None
    ticket.status = "available"
    event = db.query(_models.Event).filter(_models.Event.id == ticket.event_id).first()
    event.available_tickets += 1
    db.commit()
    db.refresh(ticket)
    db.refresh(event)
    return _schemas.TicketWithEvent.from_orm(ticket)

async def reserve_ticket(attender_id: int, ticket_id: int, db: "Session") -> _schemas.TicketWithEvent:
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    ticket.owner_id = attender_id
    ticket.status = "reserved"
    ticket.reservation_time = _dt.datetime.now().time()
    event = db.query(_models.Event).filter(_models.Event.id == ticket.event_id).first()
    event.available_tickets -= 1
    db.commit()
    db.refresh(ticket)
    db.refresh(event)
    asyncio.create_task(auto_cancel_reservations(ticket_id=ticket_id, event_id=ticket.event_id, db=db))
    return _schemas.TicketWithEvent.from_orm(ticket)

async def cancel_reservation(ticket_id: int, db: "Session") -> _schemas.TicketWithEvent:
    ticket = db.query(_models.Ticket).filter(_models.Ticket.id == ticket_id).first()
    ticket.owner_id = None
    ticket.status = "available"
    ticket.reservation_time = None
    event = db.query(_models.Event).filter(_models.Event.id == ticket.event_id).first()
    event.available_tickets += 1
    db.commit()
    db.refresh(ticket)
    db.refresh(event)
    return _schemas.TicketWithEvent.from_orm(ticket)


# PERFORMERS
async def create_performer(performer: _schemas.CreateUser, db:"Session") -> _schemas.PerformerWithEvent:
    performer = _models.Performer(**performer.dict())
    db.add(performer)
    db.commit()
    db.refresh(performer)
    return _schemas.PerformerWithEvent.from_orm(performer)

async def get_all_performers(db: "Session") -> List[_schemas.PerformerWithEvent]:
    performers = db.query(_models.Performer).all()
    return list(map(_schemas.PerformerWithEvent.from_orm, performers))

async def get_performer(performer_id: int, db: "Session") -> _schemas.PerformerWithEvent:
    performer = db.query(_models.Performer).filter(_models.Performer.id == performer_id).first()
    return performer

async def delete_performer(performer: _models.Performer, db: "Session"):
    db.delete(performer)
    db.commit()

async def update_performer(performer_data: _schemas.CreateUser, performer: _models.Performer, db: "Session") -> _schemas.PerformerWithEvent:
    performer.name = performer_data.name
    performer.surname = performer_data.surname

    db.commit()
    db.refresh(performer)

    return _schemas.PerformerWithEvent.from_orm(performer)

async def add_performer(event: _models.Event, performer: _models.Performer, db: "Session") -> _schemas.EventWithTickets:
    event.performers.append(performer)
    db.commit()
    db.refresh(event)
    return event


# ATTENDERS
async def create_attender(attender: _schemas.CreateUser, db:"Session") -> _schemas.AttenderWithTickets:
    attender = _models.Attender(**attender.dict())
    db.add(attender)
    db.commit()
    db.refresh(attender)
    return _schemas.AttenderWithTickets.from_orm(attender)

async def get_all_attenders(db: "Session") -> List[_schemas.AttenderWithTickets]:
    attenders = db.query(_models.Attender).all()
    return list(map(_schemas.AttenderWithTickets.from_orm, attenders))

async def get_attender(attender_id: int, db: "Session") -> List[_schemas.AttenderWithTickets]:
    attender = db.query(_models.Attender).filter(_models.Attender.id == attender_id).first()
    return attender

async def delete_attender(attender: _models.Attender, db: "Session"):
    db.delete(attender)
    db.commit()

async def update_attender(attender_data: _schemas.CreateUser, attender: _models.Attender, db: "Session") -> _schemas.AttenderWithTickets:
    attender.name = attender_data.name
    attender.surname = attender_data.surname

    db.commit()
    db.refresh(attender)

    return _schemas.AttenderWithTickets.from_orm(attender)

async def get_event_buy_attenders(event_id: int, db: "Session") -> List[_schemas.Attender]:
    tickets = db.query(_models.Ticket).filter(_models.Ticket.event_id==event_id, _models.Ticket.status=='sold').all()
    owners = []
    for ticket in tickets:
        owners.append(ticket.owner_id)

    attenders = db.query(_models.Attender).filter(_models.Attender.id.in_(owners))
    
    return list(map(_schemas.Attender.from_orm, attenders))

async def get_event_reserved_ticket_attenders(event_id: int, db: "Session") -> List[_schemas.AttenderWithTickets]:
    tickets = db.query(_models.Ticket).filter(_models.Ticket.event_id == event_id, _models.Ticket.status=="reserved").all()
    attenders = []
    for ticket in tickets:
        attenders.append(ticket.owner_id)

    attenders = db.query(_models.Attender).filter(_models.Attender.id.in_(attenders))

    return list(map(_schemas.AttenderWithTickets.from_orm, attenders))