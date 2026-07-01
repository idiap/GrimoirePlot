# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

from grimoireplot.plot_live_update import (
    layout_relayout_diff,
    normalize_figure_dict,
    trace_data_appended,
)


class TestTraceDataAppended:
    def test_detects_appended_points(self):
        old = {"type": "scatter", "x": [0, 1], "y": [2, 3]}
        new = {"type": "scatter", "x": [0, 1, 2], "y": [2, 3, 4]}
        assert trace_data_appended(old, new) == ([2], [4])

    def test_no_new_points(self):
        old = {"type": "scatter", "x": [0, 1], "y": [2, 3]}
        new = {"type": "scatter", "x": [0, 1], "y": [2, 3]}
        assert trace_data_appended(old, new) == ([], [])

    def test_rejects_changed_prefix(self):
        old = {"type": "scatter", "x": [0, 1], "y": [2, 3]}
        new = {"type": "scatter", "x": [0, 9], "y": [2, 3]}
        assert trace_data_appended(old, new) is None

    def test_rejects_trace_type_change(self):
        old = {"type": "scatter", "x": [0], "y": [1]}
        new = {"type": "bar", "x": [0, 1], "y": [1, 2]}
        assert trace_data_appended(old, new) is None


class TestLayoutRelayoutDiff:
    def test_detects_title_change(self):
        old = {"title": {"text": "Old"}}
        new = {"title": {"text": "New"}}
        assert layout_relayout_diff(old, new) == {"title.text": "New"}

    def test_ignores_unchanged_layout(self):
        layout = {"title": {"text": "Same"}, "xaxis": {"title": {"text": "X"}}}
        assert layout_relayout_diff(layout, layout) == {}


class TestNormalizeFigureDict:
    def test_copies_trace_lists(self):
        fig = {
            "data": [{"type": "scatter", "x": [1, 2], "y": [3, 4]}],
            "layout": {"title": {"text": "Test"}},
        }
        normalized = normalize_figure_dict(fig)
        assert normalized["data"][0]["x"] == [1, 2]
        assert normalized["data"][0]["x"] is not fig["data"][0]["x"]
        normalized["data"][0]["x"].append(3)
        assert fig["data"][0]["x"] == [1, 2]

    def test_default_scatter_type_matches_plotly(self):
        old = {"x": [0], "y": [1]}
        new = {"type": "scatter", "x": [0, 1], "y": [1, 2]}
        assert trace_data_appended(old, new) == ([1], [2])
