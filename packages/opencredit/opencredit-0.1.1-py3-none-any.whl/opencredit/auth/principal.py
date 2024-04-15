from __future__ import annotations
from typing import Optional
import time

from opencredit.server.models import V1Principal
from opencredit.db.models import UserRecord
from opencredit.db.conn import WithDB


class Principal(WithDB):
    email: str
    display_name: str
    picture: str
    created: int
    updated: int

    def __init__(
        self,
        email: str,
        display_name: str,
        picture: str,
    ) -> None:
        found = self.find_one(email)
        if found:
            raise ValueError("user already exists")

        self.email = email
        self.display_name = display_name
        self.picture = picture
        self.created = int(time.time())
        self.updated = int(time.time())

        self.save()

    def save(self) -> None:
        for db in self.get_db():
            user_record = UserRecord(
                email=self.email,
                display_name=self.display_name,
                picture=self.picture,
                created=self.created,
                updated=self.updated,
            )
            db.add(user_record)
            db.commit()

    def to_v1_schema(self) -> V1Principal:
        return V1Principal(
            email=self.email,
            display_name=self.display_name,
            picture=self.picture,
            created=self.created,
            updated=self.updated,
        )

    @classmethod
    def from_v1_schema(cls, schema: V1Principal) -> Optional[Principal]:
        if not schema.email:
            raise ValueError("Email is required")
        if not schema.display_name:
            raise ValueError("Display name is required")
        if not schema.picture:
            raise ValueError("Picture is required")
        found = cls.find_one(schema.email)
        if found:
            return found

        return cls(schema.email, schema.display_name, schema.picture)

    @classmethod
    def from_state(cls, state: UserRecord) -> Principal:
        new = cls.__new__(Principal)  # type: ignore
        new.email = str(state.email)
        new.display_name = str(state.display_name)
        new.picture = str(state.picture)
        new.created = state.created  # type: ignore
        new.updated = state.updated  # type: ignore

        return new

    @classmethod
    def find_one(cls, id: str) -> Optional[Principal]:
        for db in cls.get_db():
            user_record = db.query(UserRecord).where(UserRecord.email == id).first()
            if not user_record:
                return None
            return cls.from_state(user_record)
