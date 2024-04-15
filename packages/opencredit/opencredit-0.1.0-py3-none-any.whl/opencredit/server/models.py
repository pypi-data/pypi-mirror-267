from turtle import update
from typing import Optional, Dict, List

from pydantic import BaseModel


class V1Principal(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    handle: Optional[str] = None
    picture: Optional[str] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    token: Optional[str] = None


class V1Balance(BaseModel):
    credit: str
    email: str
    amount: float = 0.0
    minimum: float = 0.0
    maximum: float = 1000.0
    topup_minimum: Optional[float] = None
    topup_amount: Optional[float] = None
    created: float
    updated: float


class V1User(BaseModel):
    email: str
    user_minimum: float = 0.0
    user_maximum: float = 1000.0
    balances: Dict[str, V1Balance] = {}
    metadata: dict = {}


class V1Credit(BaseModel):
    name: str
    description: str
    user_min: float = 0.0
    user_max: float = 1000.0
    user_start: float = 0.0
    principals: List[str] = []
    created: float
    updated: float


class V1Transaction(BaseModel):
    email: str
    credit: str
    amount: float
    starting_balance: float
    ending_balance: float
    meter: Optional[str] = None
    created: float


class V1Meter(BaseModel):
    credit: str
    name: str
    unit: str
    cost: float
    description: Optional[str]
    principals: Optional[List[str]] = []
