from typing import List
import fastapi as _fastapi
import schemas as _schemas
import mongoModels as _mongoM
import services as _services
import models as _models
import mongoSchemas as _mongoS
import sqlalchemy.orm as _orm
import datetime as _dt
from database import reviews_collection, description_collection
from bson import ObjectId

app = _fastapi.FastAPI()
_services._add_tables()
tags_metadata = [
    {"name": "Events"},
    {"name": "Tickets"},
    {"name": "Attenders"},
    {"name": "Performers"},
    {"name": "MongoDB"},
]

# EVENTS
@app.post("/api/events/", response_model=_schemas.EventWithTickets, tags=["Events"])
async def create_event(event: _schemas.CreateEvent, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_event(event=event, db=db)

@app.get("/api/events/", response_model=List[_schemas.EventWithTickets], tags=["Events"])
async def get_events(db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_all_events(db=db) 

@app.get("/api/events/{event_id}/", response_model=_schemas.EventWithTickets, tags=["Events"])
async def get_event(event_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    event = await _services.get_event(event_id=event_id, db=db)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event does not exist")

    return event

@app.delete("/api/events/{event_id}/", tags=["Events"])
async def delete_event(event_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    event = await _services.get_event(event_id=event_id, db=db)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event does not exist")
    await _services.delete_event(event, db=db)
    
    return "Event has been successfully deleted"

@app.put("/api/events/{event_id}/", response_model=_schemas.EventWithTickets, tags=["Events"])
async def update_event(event_id: int, event_data:_schemas.CreateEvent, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    event = await _services.get_event(event_id=event_id, db=db)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event does not exist")
    
    return await _services.update_event(event_data=event_data, event=event, db=db)

@app.patch("/api/events/{event_id}/{performer_id}", response_model=_schemas.EventWithTickets, tags=["Events"])
async def add_performer(event_id: int, performer_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    performer = db.query(_models.Performer).filter(_models.Performer.id == performer_id).first()
    event = db.query(_models.Event).filter(_models.Event.id == event_id).first()
    if not performer:
        raise _fastapi.HTTPException(status_code=404, detail="Performer does not exist")
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event does not exist")
    
    return await _services.add_performer(performer=performer, event=event, db=db)

@app.get("/api/events/{event_id}/attenders/", response_model=List[_schemas.Attender], tags=["Events"])
async def get_event_attenders(event_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_event_buy_attenders(event_id=event_id, db=db)

@app.get("/api/future-events/", response_model=List[_schemas.EventWithTickets], tags=["Events"])
async def get_2_months_ahead_events_(db: _orm.Session=_fastapi.Depends(_services.get_db)):
    date_now = _dt.datetime.now()
    return await _services.get_2_months_ahead_events(date=date_now, db=db)

@app.get("/api/event/{event_id}/attenders", response_model=List[_schemas.AttenderWithTickets], tags=["Events"])
async def get_event_reserved_tickets_attenders(event_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    attenders = await _services.get_event_reserved_ticket_attenders(event_id=event_id, db=db)

    return attenders


# TICKETS
@app.post("/api/tickets/", response_model=_schemas.Ticket, tags=["Tickets"])
async def create_ticket(ticket: _schemas.CreateTicket, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_ticket(ticket=ticket, db=db)

@app.get("/api/tickets/", response_model=List[_schemas.TicketWithEvent], tags=["Tickets"])
async def get_tickets(db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_all_tickets(db=db) 

@app.get("/api/tickets/{ticket_id}/", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def get_ticket(ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail=f"Ticket by id {ticket_id} does not exist")

    return ticket

@app.delete("/api/tickets/{ticket_id}/", tags=["Tickets"])
async def delete_ticket(ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    await _services.delete_ticket(ticket, db=db)
    
    return "Ticket has been successfully deleted"

@app.put("/api/tickets/{ticket_id}/", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def update_ticket(ticket_id: int, ticket_data:_schemas.CreateTicket, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    
    return await _services.update_ticket(ticket_data=ticket_data, ticket=ticket, db=db)

@app.patch("/api/buy-ticket/{attender_id}/{ticket_id}", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def buy_ticket(attender_id: int, ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    if ticket.status == 'reserved' and ticket.owner_id != attender_id:
        raise _fastapi.HTTPException(status_code=403, detail="Ticket has been reserved by another attender")
    
    return await _services.buy_ticket(ticket_id=ticket_id, attender_id=attender_id, db=db)

@app.patch("/api/return-ticket/{attender_id}/{ticket_id}", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def return_ticket(attender_id: int, ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    
    return await _services.return_ticket(ticket_id=ticket_id, attender_id=attender_id, db=db)

@app.patch("/api/reserve-ticket/{attender_id}/{ticket_id}", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def reserve_ticket(attender_id: int, ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    if ticket.status == 'reserved':
        raise _fastapi.HTTPException(status_code=403, detail="Ticket has been already reserved")
    
    return await _services.reserve_ticket(ticket_id=ticket_id, attender_id=attender_id, db=db)

@app.patch("/api/cancel-reservation/{attender_id}/{ticket_id}", response_model=_schemas.TicketWithEvent, tags=["Tickets"])
async def cancel_reservation(attender_id: int, ticket_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    ticket = await _services.get_ticket(ticket_id=ticket_id, db=db)
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    if not ticket:
        raise _fastapi.HTTPException(status_code=404, detail="Ticket does not exist")
    if ticket.status != 'reserved':
        raise _fastapi.HTTPException(status_code=403, detail="Ticket has not been reserved yet")
    if ticket.status == 'reserved' and ticket.owner_id != attender_id:
        raise _fastapi.HTTPException(status_code=403, detail="No registration for this ticket by attender {attender_id}")
    
    return await _services.cancel_reservation(ticket_id=ticket_id, db=db)


# PERFORMERS
@app.post("/api/performers/", response_model=_schemas.PerformerWithEvent, tags=["Performers"])
async def create_performer(performer: _schemas.CreateUser, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_performer(performer=performer, db=db)

@app.get("/api/performers/", response_model=List[_schemas.PerformerWithEvent], tags=["Performers"])
async def get_performers(db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_all_performers(db=db) 

@app.get("/api/performers/{performer_id}/", response_model=_schemas.PerformerWithEvent, tags=["Performers"])
async def get_performer(performer_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    performer = await _services.get_performer(performer_id=performer_id, db=db)
    if not performer:
        raise _fastapi.HTTPException(status_code=404, detail="Performer does not exist")

    return performer

@app.delete("/api/performers/{performer_id}/", tags=["Performers"])
async def delete_performer(performer_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    performer = await _services.get_performer(performer_id=performer_id, db=db)
    if not performer:
        raise _fastapi.HTTPException(status_code=404, detail="Performer does not exist")
    await _services.delete_performer(performer, db=db)
    
    return "Performer has been successfully deleted"

@app.put("/api/performers/{performer_id}/", response_model=_schemas.PerformerWithEvent, tags=["Performers"])
async def update_performer(performer_id: int, performer_data:_schemas.CreateUser, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    performer = await _services.get_performer(performer_id=performer_id, db=db)
    if not performer:
        raise _fastapi.HTTPException(status_code=404, detail="Performer does not exist")
    
    return await _services.update_performer(performer_data=performer_data, performer=performer, db=db)


# ATTENDERS
@app.post("/api/attenders/", response_model=_schemas.AttenderWithTickets, tags=["Attenders"])
async def create_attender(attender: _schemas.CreateUser, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_attender(attender=attender, db=db)

@app.get("/api/attenders/", response_model=List[_schemas.AttenderWithTickets], tags=["Attenders"])
async def get_attenders(db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_all_attenders(db=db) 

@app.get("/api/attenders/{attender_id}/", response_model=_schemas.AttenderWithTickets, tags=["Attenders"])
async def get_attender(attender_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")

    return attender

@app.delete("/api/attenders/{attender_id}/", tags=["Attenders"])
async def delete_attender(attender_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    await _services.delete_attender(attender, db=db)
    
    return "Attender has been successfully deleted"

@app.put("/api/attenders/{attender_id}/", response_model=_schemas.AttenderWithTickets, tags=["Attenders"])
async def update_attender(attender_id: int, attender_data:_schemas.CreateUser, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    attender = await _services.get_attender(attender_id=attender_id, db=db)
    if not attender:
        raise _fastapi.HTTPException(status_code=404, detail="Attender does not exist")
    
    return await _services.update_attender(attender_data=attender_data, attender=attender, db=db)

# MONGODB DESCRIPTION
@app.get("/api/descriptions/", tags=["MongoDB"])
async def get_descriptions():
    descriptions = _mongoS.list_descriptions(description_collection.find())
    return descriptions

@app.get("/api/descriptions/{event_id}/", tags=["MongoDB"])
async def get_description(event_id: int):
    # event_description = _mongoS.list_descriptions(description_collection.find_one({"event_id": event_id}, {"event_id":1, "description":1}))
    print(event_id)
    a = description_collection.find({"event_id": event_id})
    print(a)
    event_description = _mongoS.list_descriptions(a)
    print(event_description)
    return event_description

@app.post("/api/descriptions/", tags=["MongoDB"])
async def post_description(event_desc: _mongoM.EventDescription):
    description_collection.insert_one(dict(event_desc))

@app.put("/api/descriptions/{id}/", tags=["MongoDB"])
async def put_description(id: str, event_desc: _mongoM.EventDescription):
    description_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(event_desc)})

@app.delete("/api/descriptions/{id}/", tags=["MongoDB"])
async def delete_description(id: str):
    description_collection.find_one_and_delete({"_id": ObjectId(id)})