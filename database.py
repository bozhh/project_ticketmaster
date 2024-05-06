import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

DATABASE_URL = "postgresql://root:root@db:5432/fastapi_database"
MONGO_URL = "mongodb+srv://admin:mongoadmin@architecture.umi1w85.mongodb.net/?retryWrites=true&w=majority&appName=architecture"

engine = _sql.create_engine(DATABASE_URL)
client = MongoClient(MONGO_URL, server_api=ServerApi('1'))

mongodb = client.event_additions
reviews_collection = mongodb["reviews_collection"]
description_collection = mongodb["description_collection"]

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()