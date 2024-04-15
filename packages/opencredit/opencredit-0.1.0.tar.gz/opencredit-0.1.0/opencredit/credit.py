from token import OP
from typing import List, Optional
import json

from .db.conn import WithDB
from .db.models import CreditRecord
from .server.models import V1Credit
from .balance import Balance


class Credit(WithDB):
    """A type of credit"""

    def __init__(
        self,
        name: str,
        description: str,
        user_min: float = 0.0,
        user_max: float = 1000.0,
        user_start: float = 0.0,
        principals: List[str] = [],
    ) -> None:
        self._name = name
        self._description = description
        self._user_min = user_min
        self._user_max = user_max
        self._user_start = user_start
        self._principals = principals
        self._created = 0.0
        self._updated = 0.0

        self.save()

    def get_balance(self, email: str) -> Balance:
        balances = Balance.find(email=email, credit=self._name)
        if not balances:
            raise ValueError(f"Balance not found for {email}")
        return balances[0]

    def ensure_balance(
        self,
        email: str,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        start: Optional[float] = None,
    ) -> Balance:
        if not maximum:
            maximum = self._user_max
        if not minimum:
            minimum = self._user_min
        if not start:
            start = self._user_start
        balances = Balance.find(email=email, credit=self._name)
        if not balances:
            return Balance(
                credit=self._name,
                email=email,
                amount=start,
                minimum=minimum,
                maximum=maximum,
            )
        else:
            balance = balances[0]
            if balance.minimum != minimum or balance.maximum != maximum:
                balance.minimum = minimum
                balance.maximum = maximum
                balance.save()

            return balance

    def to_schema(self) -> V1Credit:
        return V1Credit(
            name=self._name,
            description=self._description,
            user_min=self._user_min,
            user_max=self._user_max,
            user_start=self._user_start,
            principals=self._principals,
            created=self._created,
            updated=self._updated,
        )

    @classmethod
    def from_schema(cls, schema: V1Credit) -> "Credit":
        out = cls.__new__(Credit)  # type: ignore
        out._name = schema.name
        out._description = schema.description
        out._user_min = schema.user_min
        out._user_max = schema.user_max
        out._user_start = schema.user_start
        out._principals = schema.principals
        return out

    def to_record(self) -> CreditRecord:
        return CreditRecord(
            name=self._name,
            description=self._description,
            user_min=self._user_min,
            user_max=self._user_max,
            user_start=self._user_start,
            principals=json.dumps(self._principals),
        )

    @classmethod
    def from_record(cls, record: CreditRecord) -> "Credit":
        out = cls.__new__(Credit)  # type: ignore
        out._name = record.name
        out._description = record.description
        out._user_min = record.user_min
        out._user_max = record.user_max
        out._user_start = record.user_start
        out._principals = json.loads(str(record.principals))
        out._created = record.created.timestamp()  # type: ignore
        out._updated = record.updated.timestamp()  # type: ignore
        return out

    def save(self) -> None:
        for session in self.get_db():
            if session:
                record = self.to_record()
                session.merge(record)
                session.commit()

    @classmethod
    def find(cls, **kwargs) -> list["Credit"]:
        for session in cls.get_db():
            records = session.query(CreditRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        raise ValueError("No session")

    @classmethod
    def delete(cls, name: str) -> None:
        for session in cls.get_db():
            if session:
                record = session.query(CreditRecord).filter_by(name=name).first()
                if record:
                    session.delete(record)
                    session.commit()

    def update(self, model: V1Credit) -> None:
        updated = False

        if self.user_min != model.user_min:
            self.user_min = model.user_min
            updated = True

        if self.user_max != model.user_max:
            self.user_max = model.user_max
            updated = True

        if self.user_start != model.user_start:
            self.user_start = model.user_start
            updated = True

        if self.principals != model.principals:
            self.principals = model.principals
            updated = True

        if updated:
            self.save()
