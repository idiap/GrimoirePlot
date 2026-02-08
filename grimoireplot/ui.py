"""module for nicegui UI components"""

import json
from nicegui import ui
from grimoireplot.models import (
    get_all_grimoires,
    delete_grimoire,
    delete_chapter,
    delete_plot,
    get_plots_for_chapter,
    Grimoire,
    Chapter,
    Plot,
)

# Store refreshable instances for each chapter's plots
_chapter_plot_refreshables: dict[str, ui.refreshable] = {}


def refresh_chapter_plots(chapter_name: str) -> bool:
    """Refresh only the plots for a specific chapter.

    Returns True if the chapter was found and refreshed, False otherwise.
    """
    if chapter_name in _chapter_plot_refreshables:
        _chapter_plot_refreshables[chapter_name].refresh()
        return True
    return False


def refresh_all_chapter_plots():
    """Refresh all chapter plot areas."""
    for refreshable in _chapter_plot_refreshables.values():
        refreshable.refresh()


def clear_chapter_refreshable(chapter_name: str):
    """Remove a chapter's refreshable from the registry."""
    _chapter_plot_refreshables.pop(chapter_name, None)


def clear_all_chapter_refreshables():
    """Clear all chapter refreshables (called on full dashboard refresh)."""
    _chapter_plot_refreshables.clear()


def _confirm_delete(name: str, delete_fn, on_deleted=None):
    """Show a confirmation dialog before deleting.

    Args:
        name: The name of the item to delete.
        delete_fn: Function to call to perform the deletion.
        on_deleted: Optional callback to call after deletion. If None, refreshes the whole dashboard.
    """

    def do_delete():
        delete_fn(name)
        dialog.close()
        if on_deleted:
            on_deleted()
        else:
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
    # Clear stale refreshables since we're rebuilding the entire UI
    clear_all_chapter_refreshables()

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
                ui.badge("x").props("floating rounded color=red text-white").on(
                    "click",
                    lambda _, g=grimoire: _confirm_delete(g.name, delete_grimoire),
                )
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
                ui.badge("x").props("floating rounded color=red text-white").on(
                    "click",
                    lambda _, c=chapter: _confirm_delete(c.name, delete_chapter),
                )
        tabs = list(chapter_tabs)

    # Create tab panels for each chapter
    with ui.tab_panels(chapter_tabs, value=tabs[0] if tabs else None).classes("w-full"):
        for chapter in grimoire.chapters:
            with ui.tab_panel(chapter.name):
                render_chapter(chapter)


def render_chapter(chapter: Chapter):
    """Render a chapter with its plots using a refreshable grid."""
    chapter_name = chapter.name

    @ui.refreshable
    def chapter_plots_ui():
        """Refreshable UI for the plots in this chapter."""
        plots = get_plots_for_chapter(chapter_name)
        if not plots:
            ui.label(f"No plots in {chapter_name}").classes("text-gray-500")
            return

        # Display plots in a grid
        with ui.grid(columns=6).classes("w-full gap-2 p-2"):
            for plot in plots:
                render_plot(plot, chapter_name)

    # Store the refreshable for this chapter
    _chapter_plot_refreshables[chapter_name] = chapter_plots_ui

    # Render the plots
    chapter_plots_ui()


def render_plot(plot: Plot, chapter_name: str | None = None):
    """Render a single plot."""

    def on_deleted():
        """Callback after plot is deleted - refresh only this chapter's plots."""
        if chapter_name:
            refresh_chapter_plots(chapter_name)
        else:
            dashboard_ui.refresh()

    try:
        fig = json.loads(plot.json_data)
        with ui.element("div").classes("w-full relative"):
            ui.plotly(fig).classes("w-full")
            ui.badge("x").props("floating rounded color=red text-white").on(
                "click",
                lambda _, p=plot: _confirm_delete(
                    p.name, delete_plot, on_deleted=on_deleted
                ),
            )
    except json.JSONDecodeError:
        ui.label(f"Invalid plot data: {plot.name}").classes("text-red-500")
