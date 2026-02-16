# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

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
from grimoireplot.ui_elements import (
    create_tabs,
    create_tab_panels,
    create_tab_panel,
    create_delete_badge,
    create_plot_grid,
    create_plot_container,
    create_plotly_chart,
    create_empty_state,
    create_header,
    create_page_container,
    create_glass_card,
    create_label,
    create_btn_ghost,
    create_btn_danger,
)

# Store refreshable instances for each chapter's plots
_chapter_plot_refreshables: dict[tuple[str, str], ui.refreshable] = {}


def refresh_chapter_plots(grimoire_name: str, chapter_name: str) -> bool:
    """Refresh only the plots for a specific chapter.

    Returns True if the chapter was found and refreshed, False otherwise.
    """
    key = (grimoire_name, chapter_name)
    if key in _chapter_plot_refreshables:
        _chapter_plot_refreshables[key].refresh()
        return True
    return False


def refresh_all_chapter_plots():
    """Refresh all chapter plot areas."""
    for refreshable in _chapter_plot_refreshables.values():
        refreshable.refresh()


def clear_chapter_refreshable(grimoire_name: str, chapter_name: str):
    """Remove a chapter's refreshable from the registry."""
    _chapter_plot_refreshables.pop((grimoire_name, chapter_name), None)


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

    with ui.dialog() as dialog:
        with create_glass_card():
            create_label(f"Delete '{name}'?").classes("text-xl font-bold mb-4")
            create_label("This action cannot be undone.").classes("text-slate-400 mb-6")
            with ui.row().classes("justify-end gap-3"):
                create_btn_ghost("Cancel", on_click=dialog.close)
                create_btn_danger("Delete", on_click=do_delete, icon="delete")
    dialog.open()


@ui.refreshable
def dashboard_ui():
    """Top level component that builds the dashboard from database."""
    # Clear stale refreshables since we're rebuilding the entire UI
    clear_all_chapter_refreshables()

    with create_page_container():
        # Header
        create_header("GrimoirePlot", "Your magical data visualization dashboard")

        grimoires = get_all_grimoires()

        if not grimoires:
            create_empty_state(
                "No grimoires found. Add some plots to get started!",
                icon="auto_stories",
            )
            return

        # Create tabs for each grimoire
        with create_tabs() as grimoire_tabs:
            for grimoire in grimoires:
                with ui.tab(grimoire.name).classes("rounded-lg") as tab:
                    tab.style("color: #94A3B8;")
                    create_delete_badge(
                        lambda _, g=grimoire: _confirm_delete(g.name, delete_grimoire)
                    )
            tabs = list(grimoire_tabs)

        # Create tab panels for each grimoire
        with create_tab_panels(grimoire_tabs, value=tabs[0] if tabs else None):
            for grimoire in grimoires:
                with create_tab_panel(grimoire.name):
                    render_grimoire(grimoire)


def render_grimoire(grimoire: Grimoire):
    """Render a grimoire with its chapters."""
    if not grimoire.chapters:
        create_empty_state(f"No chapters in {grimoire.name}", icon="book")
        return

    grimoire_name = grimoire.name

    # Create tabs for each chapter
    with create_tabs() as chapter_tabs:
        for chapter in grimoire.chapters:
            with ui.tab(chapter.name).classes("rounded-lg") as tab:
                tab.style("color: #94A3B8;")
                create_delete_badge(
                    lambda _, g=grimoire_name, c=chapter: _confirm_delete(
                        c.name, lambda name: delete_chapter(g, name)
                    )
                )
        tabs = list(chapter_tabs)

    # Create tab panels for each chapter
    with create_tab_panels(chapter_tabs, value=tabs[0] if tabs else None):
        for chapter in grimoire.chapters:
            with create_tab_panel(chapter.name):
                render_chapter(chapter, grimoire_name)


def render_chapter(chapter: Chapter, grimoire_name: str):
    """Render a chapter with its plots using a refreshable grid."""
    chapter_name = chapter.name

    @ui.refreshable
    def chapter_plots_ui():
        """Refreshable UI for the plots in this chapter."""
        plots = get_plots_for_chapter(grimoire_name, chapter_name)
        if not plots:
            create_empty_state(f"No plots in {chapter_name}", icon="insert_chart")
            return

        # Display plots in a responsive grid
        with create_plot_grid(columns=2):
            for plot in plots:
                render_plot(plot, grimoire_name, chapter_name)

    # Store the refreshable for this chapter
    _chapter_plot_refreshables[(grimoire_name, chapter_name)] = chapter_plots_ui

    # Render the plots
    chapter_plots_ui()


def render_plot(plot: Plot, grimoire_name: str, chapter_name: str):
    """Render a single plot."""

    def on_deleted():
        """Callback after plot is deleted - refresh only this chapter's plots."""
        refresh_chapter_plots(grimoire_name, chapter_name)

    try:
        fig = json.loads(plot.json_data)
        with create_plot_container():
            create_plotly_chart(fig)
            create_delete_badge(
                lambda _, g=grimoire_name, c=chapter_name, p=plot: _confirm_delete(
                    p.name, lambda name: delete_plot(g, c, name), on_deleted=on_deleted
                )
            )
    except json.JSONDecodeError:
        with create_plot_container():
            create_label(f"Invalid plot data: {plot.name}").classes("text-red-400")
