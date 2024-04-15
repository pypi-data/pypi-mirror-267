from typing import Optional

from .db.conn import WithDB
from .db.models import TransactionRecord
from .server.models import V1Transaction


class Transaction(WithDB):
    """A financial transaction record"""

    def __init__(
        self,
        email: str,
        credit: str,
        amount: float,
        starting_balance: float,
        ending_balance: float,
        meter: Optional[str] = None,
    ) -> None:
        self._email = email
        self._credit = credit
        self._amount = amount
        self._starting_balance = starting_balance
        self._ending_balance = ending_balance
        self._created = 0.0
        self._meter = meter

        self.save()

    def to_schema(self) -> V1Transaction:
        return V1Transaction(
            email=self._email,
            credit=self._credit,
            amount=self._amount,
            starting_balance=self._starting_balance,
            ending_balance=self._ending_balance,
            meter=self._meter,
            created=self._created,
        )

    @classmethod
    def from_schema(cls, schema: V1Transaction) -> "Transaction":
        out = cls.__new__(Transaction)  # type: ignore
        out._email = schema.email
        out._credit = schema.credit
        out._amount = schema.amount
        out._starting_balance = schema.starting_balance
        out._ending_balance = schema.ending_balance
        out._created = schema.created
        out._meter = schema.meter
        return out

    def to_record(self) -> TransactionRecord:
        return TransactionRecord(
            email=self._email,
            credit=self._credit,
            amount=self._amount,
            starting_balance=self._starting_balance,
            ending_balance=self._ending_balance,
            meter=self._meter,
        )

    @classmethod
    def from_record(cls, record: TransactionRecord) -> "Transaction":
        out = cls.__new__(Transaction)  # type: ignore
        out._email = record.email
        out._credit = record.credit
        out._amount = record.amount
        out._starting_balance = record.starting_balance
        out._ending_balance = record.ending_balance
        out._created = record.created
        out._meter = record.meter
        return out

    def save(self) -> None:
        for session in self.get_db():
            if session:
                record = self.to_record()
                session.merge(record)  # Using add instead of merge for new records
                session.commit()

    @classmethod
    def find(cls, **kwargs) -> list["Transaction"]:
        for session in cls.get_db():
            records = session.query(TransactionRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        raise Exception("no session")

    @classmethod
    def delete(cls, transaction_id: int) -> None:
        for session in cls.get_db():
            if session:
                record = (
                    session.query(TransactionRecord)
                    .filter_by(id=transaction_id)
                    .first()
                )
                if record:
                    session.delete(record)
                    session.commit()
