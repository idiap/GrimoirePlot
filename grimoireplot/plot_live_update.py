# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

"""Live Plotly updates using NiceGUI's built-in plotly APIs.

Follows the patterns from NiceGUI's plotly documentation:
https://nicegui.io/documentation/plotly#plot_updates

- Dict figures with mutable trace lists (not go.Figure) for extendTraces
- ``plot.run_plot_method('extendTraces', ...)`` for append-only live data
- ``plot.run_plot_method('relayout', ...)`` for layout-only changes
- Mutate ``plot.figure`` in place + ``plot.update()`` for structural changes
  (NiceGUI calls Plotly.react on the client when config is unchanged)
"""

from __future__ import annotations

from typing import Any

from nicegui import ui

from grimoireplot.ui_elements import style_plotly_figure


def plot_uirevision(grimoire_name: str, chapter_name: str, plot_name: str) -> str:
    """Stable uirevision key so Plotly preserves axis ranges across updates."""
    return f"{grimoire_name}/{chapter_name}/{plot_name}"


def normalize_figure_dict(fig_data: dict) -> dict:
    """Return a dict figure suitable for NiceGUI live updates.

    NiceGUI recommends the declarative dict interface so trace ``x``/``y`` stay
    mutable lists that can be appended and synced with extendTraces.
    """
    normalized: dict[str, Any] = {
        "data": [],
        "layout": dict(fig_data.get("layout", {})),
    }
    if "config" in fig_data:
        normalized["config"] = dict(fig_data["config"])

    for trace in fig_data.get("data", []):
        trace_copy = dict(trace)
        for axis in ("x", "y"):
            values = trace.get(axis)
            if isinstance(values, list):
                trace_copy[axis] = list(values)
        normalized["data"].append(trace_copy)

    return normalized


def prepare_figure(fig_data: dict, uirevision: str) -> dict:
    """Normalize, theme, and set uirevision on incoming figure data."""
    styled = style_plotly_figure(normalize_figure_dict(fig_data))
    styled["layout"]["uirevision"] = uirevision
    return styled


def _title_text(layout: dict) -> str | None:
    title = layout.get("title")
    if isinstance(title, dict):
        return title.get("text")
    if isinstance(title, str):
        return title
    return None


def _axis_title_text(layout: dict, axis: str) -> str | None:
    axis_layout = layout.get(axis, {})
    if not isinstance(axis_layout, dict):
        return None
    title = axis_layout.get("title")
    if isinstance(title, dict):
        return title.get("text")
    if isinstance(title, str):
        return title
    return None


def layout_relayout_diff(old_layout: dict, new_layout: dict) -> dict[str, Any]:
    """Return plotly.js relayout keys for layout fields that changed."""
    diff: dict[str, Any] = {}

    new_title = _title_text(new_layout)
    if _title_text(old_layout) != new_title:
        diff["title.text"] = new_title

    for axis in ("xaxis", "yaxis"):
        new_axis_title = _axis_title_text(new_layout, axis)
        if _axis_title_text(old_layout, axis) != new_axis_title:
            diff[f"{axis}.title.text"] = new_axis_title

    return diff


def _trace_type(trace: dict) -> str:
    return trace.get("type", "scatter")


def trace_data_appended(
    old_trace: dict, new_trace: dict
) -> tuple[list[Any], list[Any]] | None:
    """Return appended (x, y) if new_trace extends old_trace, else None."""
    if _trace_type(old_trace) != _trace_type(new_trace):
        return None

    old_x, old_y = old_trace.get("x", []), old_trace.get("y", [])
    new_x, new_y = new_trace.get("x", []), new_trace.get("y", [])

    if not isinstance(old_x, list) or not isinstance(new_x, list):
        return None
    if not isinstance(old_y, list) or not isinstance(new_y, list):
        return None
    if len(new_x) < len(old_x) or len(new_y) < len(old_y):
        return None
    if new_x[: len(old_x)] != old_x or new_y[: len(old_y)] != old_y:
        return None

    return (new_x[len(old_x) :], new_y[len(old_y) :])


def _figure_dict(chart: ui.plotly) -> dict | None:
    figure = chart.figure
    return figure if isinstance(figure, dict) else None


def try_extend_traces_update(
    chart: ui.plotly, new_fig_data: dict, uirevision: str
) -> bool:
    """Use NiceGUI's run_plot_method('extendTraces') when traces only grow."""
    current = _figure_dict(chart)
    if current is None:
        return False

    styled = prepare_figure(new_fig_data, uirevision)

    old_data = current.get("data", [])
    new_data = styled.get("data", [])
    if len(old_data) != len(new_data) or not old_data:
        return False

    extend_x: list[list[Any]] = []
    extend_y: list[list[Any]] = []
    trace_indices: list[int] = []

    for index, (old_trace, new_trace) in enumerate(zip(old_data, new_data)):
        appended = trace_data_appended(old_trace, new_trace)
        if appended is None:
            return False
        added_x, added_y = appended
        if added_x:
            extend_x.append(added_x)
            extend_y.append(added_y)
            trace_indices.append(index)

    relayout_diff = layout_relayout_diff(
        current.get("layout", {}), styled.get("layout", {})
    )

    if not trace_indices and not relayout_diff:
        return True

    if trace_indices:
        chart.run_plot_method(
            "extendTraces", {"x": extend_x, "y": extend_y}, trace_indices
        )
        for trace_index, added_x, added_y in zip(trace_indices, extend_x, extend_y):
            current["data"][trace_index]["x"].extend(added_x)
            current["data"][trace_index]["y"].extend(added_y)

    if relayout_diff:
        chart.run_plot_method("relayout", relayout_diff)

    current.setdefault("layout", {}).update(styled["layout"])
    current["layout"]["uirevision"] = uirevision
    if "config" in styled:
        current["config"] = styled["config"]

    return True


def mutate_figure_and_update(
    chart: ui.plotly, new_fig_data: dict, uirevision: str
) -> None:
    """Mutate plot.figure in place and call plot.update() (Plotly.react on client)."""
    styled = prepare_figure(new_fig_data, uirevision)

    figure = _figure_dict(chart)
    if figure is None:
        chart.figure = styled
        chart.update()
        return

    figure["data"] = styled["data"]
    figure["layout"] = styled["layout"]
    if "config" in styled:
        figure["config"] = styled["config"]
    chart.update()


def update_plotly_chart(chart: ui.plotly, new_fig_data: dict, uirevision: str) -> None:
    """Pick the lightest NiceGUI/Plotly update path for the incoming figure."""
    if not try_extend_traces_update(chart, new_fig_data, uirevision):
        mutate_figure_and_update(chart, new_fig_data, uirevision)


# Backwards-compatible aliases used by ui.py
try_incremental_update = try_extend_traces_update
apply_full_chart_update = mutate_figure_and_update
