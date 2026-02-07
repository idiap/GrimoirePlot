"""module for nicegui UI components"""

import json
from nicegui import ui
from grimoireplot.models import (
    get_all_grimoires,
    delete_grimoire,
    delete_chapter,
    delete_plot,
    Grimoire,
    Chapter,
    Plot,
)


def _confirm_delete(name: str, delete_fn, refresh: bool = True):
    """Show a confirmation dialog before deleting."""

    def do_delete():
        delete_fn(name)
        dialog.close()
        if refresh:
            dashboard_ui.refresh()

    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete '{name}'?").classes("text-lg font-bold")
        with ui.row():
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Delete", on_click=do_delete, color="red")
    dialog.open()


@ui.refreshable
def dashboard_ui():
    """Top level component that builds the dashboard from database."""
    grimoires = get_all_grimoires()

    if not grimoires:
        ui.label("No grimoires found. Add some plots to get started!").classes(
            "text-lg text-gray-500"
        )
        return

    # Create tabs for each grimoire
    with ui.tabs().classes("w-full") as grimoire_tabs:
        for grimoire in grimoires:
            with ui.tab(grimoire.name):
                ui.button(
                    icon="close",
                    on_click=lambda _, g=grimoire: _confirm_delete(
                        g.name, delete_grimoire
                    ),
                ).props("flat dense round size=xs").classes("ml-1")
        tabs = list(grimoire_tabs)

    # Create tab panels for each grimoire
    with ui.tab_panels(grimoire_tabs, value=tabs[0] if tabs else None).classes(
        "w-full"
    ):
        for grimoire in grimoires:
            with ui.tab_panel(grimoire.name):
                render_grimoire(grimoire)


def render_grimoire(grimoire: Grimoire):
    """Render a grimoire with its chapters."""
    if not grimoire.chapters:
        ui.label(f"No chapters in {grimoire.name}").classes("text-gray-500")
        return

    # Create tabs for each chapter
    with ui.tabs().classes("w-full") as chapter_tabs:
        for chapter in grimoire.chapters:
            with ui.tab(chapter.name):
                ui.button(
                    icon="close",
                    on_click=lambda _, c=chapter: _confirm_delete(
                        c.name, delete_chapter
                    ),
                ).props("flat dense round size=xs").classes("ml-1")
        tabs = list(chapter_tabs)

    # Create tab panels for each chapter
    with ui.tab_panels(chapter_tabs, value=tabs[0] if tabs else None).classes("w-full"):
        for chapter in grimoire.chapters:
            with ui.tab_panel(chapter.name):
                render_chapter(chapter)


def render_chapter(chapter: Chapter):
    """Render a chapter with its plots."""
    if not chapter.plots:
        ui.label(f"No plots in {chapter.name}").classes("text-gray-500")
        return

    # Display plots in a grid
    with ui.grid(columns=6).classes("w-full gap-2 p-2"):
        for plot in chapter.plots:
            render_plot(plot)


def render_plot(plot: Plot):
    """Render a single plot."""
    try:
        fig = json.loads(plot.json_data)
        with ui.card().classes("w-full"):
            with ui.row().classes("w-full justify-end"):
                ui.button(
                    icon="close",
                    on_click=lambda _, p=plot: _confirm_delete(p.name, delete_plot),
                ).props("flat dense round size=xs color=red")
            ui.plotly(fig).classes("w-full")
    except json.JSONDecodeError:
        ui.label(f"Invalid plot data: {plot.name}").classes("text-red-500")
