from __future__ import annotations

import os
from sqlmodel import Field, Relationship, SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()


class Plot(SQLModel, table=True):
    name: str = Field(primary_key=True)
    json_data: str


class Chapter(SQLModel, table=True):
    name: str = Field(primary_key=True)

    grimoire_name: str = Field(foreign_key="grimoire.name")
    grimoire: "Grimoire" = Relationship(back_populates="chapters")


class Grimoire(SQLModel, table=True):
    name: str = Field(primary_key=True)
    secret_name: str
    age: int | None = None

    chapters: list[Chapter] = Relationship(back_populates="grimoire")


def create_db_and_tables():
    if (grimoire_db := os.getenv("GRIMOIRE_DB")) is None:
        sqlite_file_name = "database.db"
        grimoire_db = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(grimoire_db)
    SQLModel.metadata.create_all(engine)
