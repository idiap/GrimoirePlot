import os
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session
from sqlalchemy import ForeignKeyConstraint
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
    grimoire_name: str = Field(primary_key=True, foreign_key="grimoire.name")

    grimoire: Grimoire = Relationship(back_populates="chapters")

    plots: list["Plot"] = Relationship(back_populates="chapter", cascade_delete=True)


class Plot(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["chapter_name", "grimoire_name"], ["chapter.name", "chapter.grimoire_name"]
        ),
    )

    name: str = Field(primary_key=True)
    chapter_name: str = Field(primary_key=True)
    grimoire_name: str = Field(primary_key=True)
    json_data: str
    created_at: datetime = Field(default_factory=datetime.now)

    chapter: Chapter = Relationship(back_populates="plots")


def get_engine():
    if os.getenv("GRIMOIRE_TEST", "").lower() in ("1", "true", "yes"):
        sqlite_file_name = "database-deleteme.db"
        grimoire_db = f"sqlite:///{sqlite_file_name}"
    elif (grimoire_db := os.getenv("GRIMOIRE_DB")) is None:
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
        chapter = session.get(Chapter, (chapter_name, grimoire_name))
        if chapter is None:
            chapter = Chapter(name=chapter_name, grimoire_name=grimoire_name)
            session.add(chapter)
            session.commit()
            session.refresh(chapter)

        # Get or create/replace Plot
        plot = session.get(Plot, (plot_name, chapter_name, grimoire_name))
        if plot is None:
            plot = Plot(
                name=plot_name,
                chapter_name=chapter_name,
                grimoire_name=grimoire_name,
                json_data=json_data,
            )
            session.add(plot)
        else:
            plot.json_data = json_data
            session.add(plot)

        session.commit()
        session.refresh(plot)

        return plot


def delete_plot(grimoire_name: str, chapter_name: str, plot_name: str) -> bool:
    """Delete a plot by composite key. Returns True if deleted, False if not found."""
    engine = get_engine()
    with Session(engine) as session:
        plot = session.get(Plot, (plot_name, chapter_name, grimoire_name))
        if plot is None:
            return False
        session.delete(plot)
        session.commit()
        return True


def delete_chapter(grimoire_name: str, chapter_name: str) -> bool:
    """Delete a chapter and all its plots. Returns True if deleted, False if not found."""
    engine = get_engine()
    with Session(engine) as session:
        chapter = session.get(Chapter, (chapter_name, grimoire_name))
        if chapter is None:
            return False
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
        session.delete(grimoire)
        session.commit()
        return True


def get_chapter_with_plots(grimoire_name: str, chapter_name: str) -> Optional[Chapter]:
    """Get a specific chapter with all its plots."""
    engine = get_engine()
    with Session(engine) as session:
        chapter = session.get(Chapter, (chapter_name, grimoire_name))
        if chapter:
            # Load relationships
            _ = chapter.plots
        return chapter


def get_plots_for_chapter(grimoire_name: str, chapter_name: str) -> list[Plot]:
    """Get all plots for a specific chapter."""
    engine = get_engine()
    with Session(engine) as session:
        from sqlmodel import select

        statement = select(Plot).where(
            Plot.chapter_name == chapter_name, Plot.grimoire_name == grimoire_name
        )
        return list(session.exec(statement).all())
