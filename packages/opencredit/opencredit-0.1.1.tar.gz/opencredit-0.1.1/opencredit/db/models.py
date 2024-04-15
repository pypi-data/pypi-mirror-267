import uuid
import time
import json

from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func


Base = declarative_base()


class CreditRecord(Base):
    __tablename__ = "credits"

    name = Column(String, primary_key=True)
    description = Column(String, nullable=False)
    user_min = Column(Float, default=0.0)
    user_max = Column(Float, default=1000.0)
    user_start = Column(Float, default=0.0)
    principals = Column(String, default="[]")  # Store principals as JSON-encoded lists
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def principals_list(self):
        return json.loads(str(self.principals))

    @principals_list.setter
    def principals_list(self, value):
        self.principals = json.dumps(value)


class PrincipalRecord(Base):
    __tablename__ = "principal"

    email = Column(String, unique=True, index=True, primary_key=True)
    display_name = Column(String)
    handle = Column(String)
    picture = Column(String)
    created = Column(Integer)
    updated = Column(Integer)


class UserRecord(Base):
    __tablename__ = "users"

    email = Column(
        String,
        primary_key=True,
        unique=True,
        index=True,
    )
    user_minimum = Column(Float, default=0.0)
    user_maximum = Column(Float, default=1000.0)
    balance = Column(Float, default=0.0)
    _metadata = Column(String, nullable=True)


class BalanceRecord(Base):
    __tablename__ = "balances"

    email = Column(String, primary_key=True)
    credit = Column(String, nullable=False)
    amount = Column(Float, default=0.0)
    minimum = Column(Float, default=0.0)
    maximum = Column(Float, default=1000.0)
    topup_minimum = Column(Float, default=None, nullable=True)
    topup_amount = Column(Float, default=None, nullable=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())


class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    credit = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    starting_balance = Column(Float, nullable=False)
    ending_balance = Column(Float, nullable=False)
    meter = Column(String, nullable=True)
    created = Column(DateTime, default=func.now())


class MeterRecord(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    credit = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    principals = Column(String, default="[]")  # JSON-encoded list of principals

    @property
    def principals_list(self):
        return json.loads(str(self.principals))

    @principals_list.setter
    def principals_list(self, value):
        self.principals = json.dumps(value)
