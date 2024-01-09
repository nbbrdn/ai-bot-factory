from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model:
    created_at = Column(DateTime, default=datetime.today())
    updated_at = Column(DateTime, onupdate=datetime.today())
