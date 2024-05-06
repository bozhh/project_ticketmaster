import datetime as _dt
import sqlalchemy as _sql
import database as _database
import sqlalchemy.orm as _orm

event_performer = _sql.Table("event_performer", _database.Base.metadata,
                             _sql.Column("event_id", _sql.Integer, _sql.ForeignKey("events.id")),
                             _sql.Column("performer_id", _sql.Integer, _sql.ForeignKey("performers.id")))

class Event(_database.Base):
    __tablename__ = "events"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True, autoincrement=True)
    name = _sql.Column(_sql.String)
    date = _sql.Column(_sql.Date)
    time = _sql.Column(_sql.Time)
    venue = _sql.Column(_sql.String)
    available_tickets = _sql.Column(_sql.Integer)
    tickets = _orm.relationship('Ticket', backref='event')
    performers = _orm.relationship('Performer', secondary=event_performer, backref='performers')

class Attender(_database.Base):
    __tablename__ = "attenders"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True, autoincrement=True)
    name = _sql.Column(_sql.String)
    surname = _sql.Column(_sql.String)
    tickets = _orm.relationship('Ticket', backref='owner')

class Performer(_database.Base):
    __tablename__ = "performers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True, autoincrement=True)
    name = _sql.Column(_sql.String)
    surname = _sql.Column(_sql.String)

class Ticket(_database.Base):
    __tablename__ = "tickets"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True, autoincrement=True)
    price = _sql.Column(_sql.Float)
    type = _sql.Column(_sql.String)
    status = _sql.Column(_sql.String)
    seat_no = _sql.Column(_sql.Integer)
    reservation_time = _sql.Column(_sql.Time)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('attenders.id'))
    event_id = _sql.Column(_sql.Integer, _sql.ForeignKey("events.id"))