from typing import Optional

from .db.conn import WithDB
from .db.models import BalanceRecord
from .server.models import V1Balance
from .transaction import Transaction


class Balance(WithDB):
    """A representation of a user's balance"""

    def __init__(
        self,
        credit: str,
        email: str,
        amount: float = 0.0,
        minimum: float = 0.0,
        maximum: float = 1000.0,
        topup_minimum: Optional[float] = None,
        topup_amount: Optional[float] = None,
    ) -> None:
        self._credit = credit
        self._email = email
        self._amount = amount
        self._minimum = minimum
        self._maximum = maximum
        self._topup_minimum = topup_minimum
        self._topup_amount = topup_amount
        self._created = 0.0
        self._updated = 0.0

        self.save()

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        if value < self._minimum or value > self._maximum:
            raise ValueError(
                f"Balance must be between {self._minimum} and {self._maximum}."
            )
        self._amount = value

    @property
    def minimum(self) -> float:
        return self._minimum

    @minimum.setter
    def minimum(self, value: float) -> None:
        if value < 0:
            raise ValueError("Minimum balance cannot be negative.")
        self._minimum = value

    @property
    def maximum(self) -> float:
        return self._maximum

    @maximum.setter
    def maximum(self, value: float) -> None:
        if value < self._minimum:
            raise ValueError("Maximum balance cannot be less than the minimum balance.")
        self._maximum = value

    def add(self, value: float, meter: Optional[str] = None) -> None:
        if value < 0:
            raise ValueError("Cannot add negative amount.")
        start_balance = self.amount
        new_balance = self.amount + value
        if new_balance < self._minimum or new_balance > self._maximum:
            raise ValueError(
                f"Balance must be between {self._minimum} and {self._maximum}."
            )
        try:
            self._amount = new_balance
            Transaction(
                self._email, self._credit, value, start_balance, new_balance, meter
            )
            self.save()
        except Exception:
            self._amount = start_balance
            raise

    def subtract(self, value: float, meter: Optional[str] = None) -> None:
        if value < 0:
            raise ValueError("Cannot subtract negative amount.")
        start_balance = self.amount
        if self.amount - value < self._minimum:
            raise ValueError("Cannot subtract more than the allowed minimum balance.")
        try:
            self._amount -= value
            Transaction(
                self._email, self._credit, value, start_balance, self._amount, meter
            )
            self.save()
        except Exception:
            self._amount = start_balance
            raise

    def to_schema(self) -> V1Balance:
        return V1Balance(
            credit=self._credit,
            email=self._email,
            amount=self._amount,
            minimum=self.minimum,
            maximum=self.maximum,
            topup_minimum=self._topup_minimum,
            topup_amount=self._topup_amount,
            created=self._created,
            updated=self._updated,
        )

    @classmethod
    def from_schema(cls, schema: V1Balance) -> "Balance":
        out = cls.__new__(Balance)  # type: ignore
        out._credit = schema.credit
        out._email = schema.email
        out._amount = schema.amount
        out._minimum = schema.minimum
        out._maximum = schema.maximum
        out._topup_minimum = schema.topup_minimum
        out._topup_amount = schema.topup_amount

        return out

    def to_record(self) -> BalanceRecord:
        return BalanceRecord(
            email=self._email,
            credit=self._credit,
            amount=self.amount,
            minimum=self.minimum,
            maximum=self.maximum,
            topup_minimum=self._topup_minimum,
            topup_amount=self._topup_amount,
        )

    @classmethod
    def from_record(cls, record: BalanceRecord) -> "Balance":
        out = cls.__new__(Balance)  # type: ignore
        out._email = record.email  # type: ignore
        out._credit = record.credit  # type: ignore
        out._amount = record.amount  # type: ignore
        out._minimum = record.minimum  # type: ignore
        out._maximum = record.maximum  # type: ignore
        out._topup_minimum = record.topup_minimum  # type: ignore
        out._topup_amount = record.topup_amount  # type: ignore
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
    def find(cls, **kwargs) -> list["Balance"]:
        for session in cls.get_db():
            records = session.query(BalanceRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        return []

    @classmethod
    def delete(cls, email: str) -> None:
        for session in cls.get_db():
            if session:
                record = session.query(BalanceRecord).filter_by(email=email).first()
                if record:
                    session.delete(record)
                    session.commit()

    def update(self, model: V1Balance) -> None:
        updated = False

        if self.amount != model.amount:
            self.amount = model.amount
            updated = True

        if self.minimum != model.minimum:
            self.minimum = model.minimum
            updated = True

        if self.maximum != model.maximum:
            self.maximum = model.maximum
            updated = True

        if self.topup_minimum != model.topup_minimum:
            self.topup_minimum = model.topup_minimum
            updated = True

        if self.topup_amount != model.topup_amount:
            self.topup_amount = model.topup_amount
            updated = True

        if updated:
            self.save()
