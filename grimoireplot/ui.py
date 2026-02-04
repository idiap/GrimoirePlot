"""module for nicegui UI components"""

import json
from nicegui import ui
from grimoireplot.models import get_all_grimoires, Grimoire, Chapter, Plot


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
        tabs = [ui.tab(grimoire.name) for grimoire in grimoires]

    # Create tab panels for each grimoire
    with ui.tab_panels(grimoire_tabs, value=tabs[0] if tabs else None).classes(
        "w-full"
    ):
        for grimoire, tab in zip(grimoires, tabs):
            with ui.tab_panel(tab):
                render_grimoire(grimoire)


def render_grimoire(grimoire: Grimoire):
    """Render a grimoire with its chapters."""
    if not grimoire.chapters:
        ui.label(f"No chapters in {grimoire.name}").classes("text-gray-500")
        return

    # Create tabs for each chapter
    with ui.tabs().classes("w-full") as chapter_tabs:
        tabs = [ui.tab(chapter.name) for chapter in grimoire.chapters]

    # Create tab panels for each chapter
    with ui.tab_panels(chapter_tabs, value=tabs[0] if tabs else None).classes("w-full"):
        for chapter, tab in zip(grimoire.chapters, tabs):
            with ui.tab_panel(tab):
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
        ui.plotly(fig).classes("w-full")
    except json.JSONDecodeError:
        ui.label(f"Invalid plot data: {plot.name}").classes("text-red-500")
