from typing import Optional, List
import json

from .db.conn import WithDB
from .balance import Balance
from .db.models import MeterRecord
from .server.models import V1Meter


class Meter(WithDB):
    """A credit usage meter"""

    def __init__(
        self,
        credit: str,
        name: str,
        unit: str,
        cost: float,
        description: str,
        principals: Optional[List[str]] = None,
    ) -> None:
        self._credit = credit
        self._name = name
        self._unit = unit
        self._cost = cost
        self._description = description
        self._principals = principals or []

        self.save()

    def tick(self, amount: float, email: str) -> None:
        balances = Balance.find(email=email, credit=self._credit)
        if not balances:
            raise ValueError("Balance not found")
        balance = balances[0]
        balance.subtract(amount * self._cost, self._name)

    def to_schema(self) -> V1Meter:
        return V1Meter(
            credit=self._credit,
            name=self._name,
            unit=self._unit,
            cost=self._cost,
            description=self._description,
            principals=self._principals,
        )

    @classmethod
    def from_schema(cls, schema: V1Meter) -> "Meter":
        out = cls.__new__(cls)
        out._credit = schema.credit
        out._name = schema.name
        out._unit = schema.unit
        out._cost = schema.cost
        out._description = schema.description
        out._principals = schema.principals
        return out

    def to_record(self) -> MeterRecord:
        return MeterRecord(
            credit=self._credit,
            name=self._name,
            unit=self._unit,
            cost=self._cost,
            description=self._description,
            principals=json.dumps(self._principals),
        )

    @classmethod
    def from_record(cls, record: MeterRecord) -> "Meter":
        out = cls.__new__(cls)
        out._credit = record.credit
        out._name = record.name
        out._unit = record.unit
        out._cost = record.cost
        out._description = record.description
        out._principals = json.loads(str(record.principals))
        return out

    def save(self) -> None:
        for session in self.get_db():
            record = self.to_record()
            session.merge(record)
            session.commit()

    @classmethod
    def find(cls, **kwargs) -> List["Meter"]:
        for session in cls.get_db():
            records = session.query(MeterRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        raise Exception("No session")

    @classmethod
    def delete(cls, meter_id: int) -> None:
        for session in cls.get_db():
            record = session.query(MeterRecord).filter_by(id=meter_id).first()
            if record:
                session.delete(record)
                session.commit()

    def update(self, model: V1Meter) -> None:
        updated = False

        # Fetch the existing MeterRecord directly rather than relying on non-primary unique fields
        for session in self.get_db():
            record = session.query(MeterRecord).filter_by(name=self._name).first()
            if not record:
                raise ValueError(f"No meter found with the name {self._name}")

            print("\n\n!!! updating")
            if record.unit != model.unit:  # type: ignore
                record.unit = model.unit  # type: ignore
                updated = True

            if record.cost != model.cost:  # type: ignore
                print("\n\n!! updating cost")
                record.cost = model.cost  # type: ignore
                updated = True

            if record.description != model.description:  # type: ignore
                record.description = model.description  # type: ignore
                updated = True

            if json.loads(record.principals) != model.principals:  # type: ignore
                record.principals = json.dumps(model.principals)
                updated = True

            if updated:
                session.commit()
