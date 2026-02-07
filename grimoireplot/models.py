import os
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()


class AddPlotRequest(SQLModel):
    grimoire_name: str
    chapter_name: str
    plot_name: str
    json_data: str


class Grimoire(SQLModel, table=True):
    name: str = Field(primary_key=True)

    chapters: list["Chapter"] = Relationship(
        back_populates="grimoire", cascade_delete=True
    )


class Chapter(SQLModel, table=True):
    name: str = Field(primary_key=True)

    grimoire_name: str = Field(foreign_key="grimoire.name")
    grimoire: Grimoire = Relationship(back_populates="chapters")

    plots: list["Plot"] = Relationship(back_populates="chapter", cascade_delete=True)


class Plot(SQLModel, table=True):
    name: str = Field(primary_key=True)
    json_data: str
    created_at: datetime = Field(default_factory=datetime.now)
    chapter_name: str = Field(foreign_key="chapter.name")
    chapter: Chapter = Relationship(back_populates="plots")


def get_engine():
    if (grimoire_db := os.getenv("GRIMOIRE_DB")) is None:
        sqlite_file_name = "database.db"
        grimoire_db = f"sqlite:///{sqlite_file_name}"
    return create_engine(grimoire_db)


def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_all_grimoires() -> list[Grimoire]:
    """Get all grimoires with their chapters and plots."""
    engine = get_engine()
    with Session(engine) as session:
        from sqlmodel import select

        statement = select(Grimoire)
        grimoires = session.exec(statement).all()
        # Ensure relationships are loaded
        result = []
        for grimoire in grimoires:
            # Access chapters to load them
            _ = grimoire.chapters
            for chapter in grimoire.chapters:
                # Access plots to load them
                _ = chapter.plots
            result.append(grimoire)
        return result


def get_grimoire_with_data(grimoire_name: str) -> Optional[Grimoire]:
    """Get a specific grimoire with all its chapters and plots."""
    engine = get_engine()
    with Session(engine) as session:
        grimoire = session.get(Grimoire, grimoire_name)
        if grimoire:
            # Load relationships
            _ = grimoire.chapters
            for chapter in grimoire.chapters:
                _ = chapter.plots
        return grimoire


def add_plot(
    grimoire_name: str, chapter_name: str, plot_name: str, json_data: str
) -> Plot:
    """Add a plot to a grimoire/chapter, creating them if they don't exist.

    If the grimoire exists, use it, else create it.
    If the chapter exists, use it, else create it.
    If the plot exists, replace it, else add it.

    TODO: check if json_data is valid plotly, if not raise exception.
    """

    engine = get_engine()

    with Session(engine) as session:
        # Get or create Grimoire
        grimoire = session.get(Grimoire, grimoire_name)
        if grimoire is None:
            grimoire = Grimoire(name=grimoire_name)
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


def delete_plot(plot_name: str) -> bool:
    """Delete a plot by name. Returns True if deleted, False if not found."""
    engine = get_engine()
    with Session(engine) as session:
        plot = session.get(Plot, plot_name)
        if plot is None:
            return False
        session.delete(plot)
        session.commit()
        return True


def delete_chapter(chapter_name: str) -> bool:
    """Delete a chapter and all its plots. Returns True if deleted, False if not found."""
    engine = get_engine()
    with Session(engine) as session:
        chapter = session.get(Chapter, chapter_name)
        if chapter is None:
            return False
        for plot in chapter.plots:
            session.delete(plot)
        session.delete(chapter)
        session.commit()
        return True


def delete_grimoire(grimoire_name: str) -> bool:
    """Delete a grimoire and all its chapters and plots. Returns True if deleted, False if not found."""
    engine = get_engine()
    with Session(engine) as session:
        grimoire = session.get(Grimoire, grimoire_name)
        if grimoire is None:
            return False
        for chapter in grimoire.chapters:
            for plot in chapter.plots:
                session.delete(plot)
            session.delete(chapter)
        session.delete(grimoire)
        session.commit()
        return True
