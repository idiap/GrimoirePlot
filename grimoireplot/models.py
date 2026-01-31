from __future__ import annotations

import os
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()


class AddPlotRequest(SQLModel):
    grimoire_name: str
    chapter_name: str
    plot_name: str
    json_data: str


class Plot(SQLModel, table=True):
    name: str = Field(primary_key=True)
    json_data: str
    created_at: datetime = Field(default_factory=datetime.now)
    chapter_name: str = Field(foreign_key="chapter.name")
    chapter: "Chapter" = Relationship(back_populates="plots")


class Chapter(SQLModel, table=True):
    name: str = Field(primary_key=True)

    plots: list[Plot] = Relationship(back_populates="chapter")

    grimoire_name: str = Field(foreign_key="grimoire.name")
    grimoire: "Grimoire" = Relationship(back_populates="chapters")


class Grimoire(SQLModel, table=True):
    name: str = Field(primary_key=True)
    secret_name: str
    age: int | None = None

    chapters: list[Chapter] = Relationship(back_populates="grimoire")


def get_engine():
    if (grimoire_db := os.getenv("GRIMOIRE_DB")) is None:
        sqlite_file_name = "database.db"
        grimoire_db = f"sqlite:///{sqlite_file_name}"
    return create_engine(grimoire_db)


def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def add_plot(
    grimoire_name: str, chapter_name: str, plot_name: str, json_data: str
) -> Plot:
    """Add a plot to a grimoire/chapter, creating them if they don't exist.

    If the grimoire exists, use it, else create it.
    If the chapter exists, use it, else create it.
    If the plot exists, replace it, else add it.
    """

    engine = get_engine()

    with Session(engine) as session:
        # Get or create Grimoire
        grimoire = session.get(Grimoire, grimoire_name)
        if grimoire is None:
            grimoire = Grimoire(name=grimoire_name, secret_name=grimoire_name)
            session.add(grimoire)
            session.commit()
            session.refresh(grimoire)

        # Get or create Chapter
        chapter = session.get(Chapter, chapter_name)
        if chapter is None:
            chapter = Chapter(name=chapter_name, grimoire_name=grimoire_name)
            session.add(chapter)
            session.commit()
            session.refresh(chapter)

        # Get or create/replace Plot
        plot = session.get(Plot, plot_name)
        if plot is None:
            plot = Plot(name=plot_name, json_data=json_data, chapter_name=chapter_name)
            session.add(plot)
        else:
            plot.json_data = json_data
            plot.chapter_name = chapter_name
            session.add(plot)

        session.commit()
        session.refresh(plot)

        return plot
