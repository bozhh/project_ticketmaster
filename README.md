# Homework 4: 🎫 Ticket Purchasing System (aka ticketmaster.com|concert.ua|...)
Author: **Kvitoslava Kolodii**

## Requirements for the system:
- DDL for creating tables in the database
- Code of the program implementing the described API. These should be REST APIs.
- Swagger documentation for the implemented APIs.
- Dockerfile for packaging your program into a container.
- Docker-compose that deploys all elements of your system (currently relational database and web server with REST API).
- Screenshots of the results of each API endpoint's operation + screenshots of database state changes after accessing each of these endpoints.

## 🤖 REST APIs to implement:
- Create, Update, Delete operations for events.
- Create, Update, Delete operations for performers.
- Create, Update, Delete operations for tickets.
- Create, Update, Delete operations for users.
- Get a list of all events available in the system.
- Get information about a ticket/event/performer by ID.
- Get information about the availability of events for the next two months, including the number of available tickets for each event, as well as events for which all tickets have already been sold or reserved.
- Reserve tickets for a specific event (maximum reservation duration - 15 minutes), if they are available and not reserved by another visitor. Until the purchase/cancellation of the reservation, the ticket is unavailable to other users.
- Get information about users who have reserved a ticket for an event with event_id.
- Get all users who purchased tickets for an event event_id on date.
- Get a list of all performers participating in events.
- Get information about the tickets purchased by a specific visitor.
- Purchase selected tickets for a specific event.
- Return a ticket. After returning the ticket, it becomes available for subsequent purchases.

## Entities to implement:
🎠 Event:
    Event Name
    
    Date
    
    Time
    
    Venue
    
    Number of Tickets

👩‍🎤 Performer:
    First Name

    Last Name

🎫 Ticket:

    Ticket Type

    Price
    
    Status (sold, available, reserved)
    
🙋 Attender:

    First Name
    
    Last Name

## 📝 What does this MR do?
- Main components: 

    🗂️ relational database "fastapi_database" (PostgreSQL);

    🐍 Python script: creates tables, runs web server, executes API endpoints, saves data to db tables;

- requirements met:

    ✅ DDL creating database;

    ✅ REST APIs, described in the requirements above;

    ✅ Swagger documentation;

    ✅ program is packaged into a Docker container and launches upon its start;

    ✅ all elements of the system are deployed by a Docker-compose

    ✅ all screenshots of the results in [this directory](https://gitlab.com/kvitK1/architecture-kolodii.git)

- implementation approach:
    - main language: python
    - REST APIs framework: FastAPI
    - SQL toolkit: SQLAlchemy
    - other modules: {datetime, pydantic, typing, asyncio}
    - venv (all installations in requirements.txt)
    - easy deployment & isolation: Docker Compose

## 🏃 'How to run?'
1. Clone the repository

`git clone https://gitlab.com/kvitK1/architecture-kolodii`

2. Go to directory `architecture-kolodii`

`cd architecture-kolodii`

3. Go to branch "homework4"

`git checkout homework4`

4. Go to directory `Ticketmaster`

`cd Ticketmaster`

4. Run this command to build docker containers from docker compose:

`docker compose up -d`

5. Run this command (don't understand how to fix when compose builds - app container exits faster than db container is built):

`docker start apz_homework2-api-1`

6. Go to [localhost](http://localhost:8000/docs), test API endpoints

## 🥂 **Results**
- Create Event

![](hw4screens/createevent1.png)
![](hw4screens/createevent2.png)
![](hw4screens/createevent3.png)

# - Get Events

![](hw4screens/getevents.png)

# - Get Event by id

![](hw4screens/geteventbyid.png)

# - Update Event

![](hw4screens/updateevent1.png)
![](hw4screens/updateevent2.png)

# - Delete Event

![](hw4screens/deleteevent.png)
![](hw4screens/deleteevent2.png)

# - Get 2 Months Ahead Events

![](hw4screens/twomonthevents.png)

# - Add Performer

![](hw4screens/addperformer1.png)
![](hw4screens/addperformer2.png)

# - Create Ticket

![](hw4screens/createticket.png)
![](hw4screens/createticket2.png)
![](hw4screens/createticket3.png)

# - Get Tickets

![](hw4screens/gettickets.png)

# - Get Ticket by id

![](hw4screens/getticketid.png)

# - Update Ticket

![](hw4screens/updateticket1.png)
![](hw4screens/updateticket2.png)
![](hw4screens/updateticket3.png)

# - Delete Ticket

![](hw4screens/deleteticket1.png)
![](hw4screens/deleteticket2.png)

# - Reserve Ticket

![](hw4screens/reserveticket1.png)
![](hw4screens/reserveticket2.png)

# - Cancel Reservation
![](hw4screens/cancelreserve1.png)
![](hw4screens/cancelreserve2.png)
![](hw4screens/cancelreserve3.png)
![](hw4screens/autocancelreservation.png)

# - Buy Ticket

![](hw4screens/buyticket1.png)
![](hw4screens/buyticket2.png)

# - Return Ticket

![](hw4screens/returnticket1.png)
![](hw4screens/returnticket2.png)

# - Create Attender

![](hw4screens/createattender1.png)
![](hw4screens/createattender2.png)

# - Get Attenders

![](hw4screens/getattenders.png)

# - Get Attender by id

![](hw4screens/getattenderbyid.png)

# - Update Attender

![](hw4screens/updateattender1.png)
![](hw4screens/updateattender2.png)

# - Delete Attender

![](hw4screens/deleteattender1.png)
![](hw4screens/deleteattender2.png)

# - Create Performer

![](hw4screens/createperformer1.png)
![](hw4screens/createperformer2.png)

# - Get Performers

![](hw4screens/getperformers.png)

# - Get Performer by id

![](hw4screens/getperformerbyid.png)

# - Update Performer

![](hw4screens/updateperformer1.png)
![](hw4screens/updateperformer2.png)

# - Delete Performer

![](hw4screens/deleteperformer.png)
![](hw4screens/deleteperformer2.png)
