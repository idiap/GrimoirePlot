# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

"""
Integration tests for GrimoirePlot.

Spawns the server with GRIMOIRE_TEST=true (uses database-deleteme.db),
pushes plots via HTTP, and verifies the database contents.
"""

import json
import os
import signal
import socket
import subprocess
import sys
import time

import plotly.graph_objects as go
import pytest
import requests
from sqlmodel import Session, create_engine, select

from grimoireplot.models import Chapter, Grimoire, Plot

TEST_DB_FILE = "database-deleteme.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_FILE}"
TEST_SECRET = "test-secret-12345"


def _find_free_port() -> int:
    """Find a free TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_server(url: str, timeout: float = 30.0, interval: float = 0.5) -> None:
    """Wait until the server is accepting connections."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return
        except requests.ConnectionError:
            pass
        time.sleep(interval)
    raise TimeoutError(f"Server at {url} did not start within {timeout}s")


def _cleanup_test_db():
    """Remove the test database file if it exists."""
    if os.path.exists(TEST_DB_FILE):
        os.unlink(TEST_DB_FILE)


@pytest.fixture(scope="session")
def server():
    """Spawn a GrimoirePlot server with GRIMOIRE_TEST=true.

    Uses database-deleteme.db. The fixture is session-scoped so the server
    is started once for all tests. The DB file is cleaned up at teardown.
    """
    _cleanup_test_db()

    port = _find_free_port()

    env = os.environ.copy()
    env["GRIMOIRE_TEST"] = "true"
    env["GRIMOIRE_SECRET"] = TEST_SECRET
    # Remove pytest env vars so NiceGUI doesn't enter screen-test mode
    for key in list(env.keys()):
        if key.startswith("PYTEST") or key.startswith("NICEGUI"):
            del env[key]

    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "from grimoireplot.main import main; main()",
            "serve",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    url = f"http://127.0.0.1:{port}"
    try:
        _wait_for_server(url)
    except TimeoutError:
        proc.kill()
        proc.wait()
        stdout = proc.stdout.read().decode() if proc.stdout else ""
        stderr = proc.stderr.read().decode() if proc.stderr else ""
        _cleanup_test_db()
        raise RuntimeError(
            f"Server failed to start.\nstdout:\n{stdout}\nstderr:\n{stderr}"
        )

    info = {
        "url": url,
        "port": port,
        "secret": TEST_SECRET,
        "db_url": TEST_DB_URL,
    }

    yield info

    # Teardown: kill server and remove test DB
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    _cleanup_test_db()


def _make_figure(title: str = "Test") -> go.Figure:
    """Create a simple Plotly figure for testing."""
    fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines")])
    fig.update_layout(title=title)
    return fig


def _read_grimoires(db_url: str) -> list[Grimoire]:
    """Read all grimoires directly from the database."""
    engine = create_engine(db_url)
    with Session(engine) as session:
        return list(session.exec(select(Grimoire)).all())


def _read_chapters(db_url: str) -> list[Chapter]:
    """Read all chapters directly from the database."""
    engine = create_engine(db_url)
    with Session(engine) as session:
        return list(session.exec(select(Chapter)).all())


def _read_plots(db_url: str) -> list[Plot]:
    """Read all plots directly from the database."""
    engine = create_engine(db_url)
    with Session(engine) as session:
        return list(session.exec(select(Plot)).all())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAddPlot:
    """Tests for pushing plots to the server and verifying the database."""

    def test_push_single_plot(self, server):
        """Push a single plot and verify it exists in the DB."""
        fig = _make_figure("Single Plot")
        resp = requests.post(
            f"{server['url']}/add_plot",
            headers={"grimoire-secret": server["secret"]},
            json={
                "grimoire_name": "g1",
                "chapter_name": "ch1",
                "plot_name": "p1",
                "json_data": fig.to_json(),
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        assert body["plot_name"] == "p1"

        # Verify database
        grimoires = _read_grimoires(server["db_url"])
        assert any(g.name == "g1" for g in grimoires)

        chapters = _read_chapters(server["db_url"])
        assert any(c.name == "ch1" and c.grimoire_name == "g1" for c in chapters)

        plots = _read_plots(server["db_url"])
        matching = [p for p in plots if p.name == "p1" and p.grimoire_name == "g1"]
        assert len(matching) == 1

        # Verify the stored JSON is valid plotly data
        stored_data = json.loads(matching[0].json_data)
        assert "data" in stored_data
        assert "layout" in stored_data

    def test_push_multiple_plots_same_chapter(self, server):
        """Push multiple plots to the same chapter and verify."""
        for i in range(3):
            fig = _make_figure(f"Multi Plot {i}")
            resp = requests.post(
                f"{server['url']}/add_plot",
                headers={"grimoire-secret": server["secret"]},
                json={
                    "grimoire_name": "g_multi",
                    "chapter_name": "ch_multi",
                    "plot_name": f"multi_plot_{i}",
                    "json_data": fig.to_json(),
                },
            )
            assert resp.status_code == 200

        plots = _read_plots(server["db_url"])
        matching = [p for p in plots if p.grimoire_name == "g_multi"]
        assert len(matching) == 3
        plot_names = {p.name for p in matching}
        assert plot_names == {"multi_plot_0", "multi_plot_1", "multi_plot_2"}

    def test_push_plots_multiple_chapters(self, server):
        """Push plots to different chapters under the same grimoire."""
        for ch in ["alpha", "beta"]:
            fig = _make_figure(f"Plot in {ch}")
            resp = requests.post(
                f"{server['url']}/add_plot",
                headers={"grimoire-secret": server["secret"]},
                json={
                    "grimoire_name": "mybook",
                    "chapter_name": ch,
                    "plot_name": f"p_{ch}",
                    "json_data": fig.to_json(),
                },
            )
            assert resp.status_code == 200

        chapters = _read_chapters(server["db_url"])
        matching = [c for c in chapters if c.grimoire_name == "mybook"]
        assert len(matching) == 2
        chapter_names = {c.name for c in matching}
        assert chapter_names == {"alpha", "beta"}

    def test_push_plots_multiple_grimoires(self, server):
        """Push plots to different grimoires and verify isolation."""
        for g in ["grimoire_a", "grimoire_b"]:
            fig = _make_figure(f"Plot in {g}")
            resp = requests.post(
                f"{server['url']}/add_plot",
                headers={"grimoire-secret": server["secret"]},
                json={
                    "grimoire_name": g,
                    "chapter_name": "ch1",
                    "plot_name": "p1",
                    "json_data": fig.to_json(),
                },
            )
            assert resp.status_code == 200

        grimoires = _read_grimoires(server["db_url"])
        grimoire_names = {g.name for g in grimoires}
        assert "grimoire_a" in grimoire_names
        assert "grimoire_b" in grimoire_names

    def test_replace_existing_plot(self, server):
        """Pushing a plot with the same name should replace its data."""
        fig1 = _make_figure("Original")
        fig2 = _make_figure("Replacement")

        for fig in [fig1, fig2]:
            resp = requests.post(
                f"{server['url']}/add_plot",
                headers={"grimoire-secret": server["secret"]},
                json={
                    "grimoire_name": "g_replace",
                    "chapter_name": "ch_replace",
                    "plot_name": "same_plot",
                    "json_data": fig.to_json(),
                },
            )
            assert resp.status_code == 200

        plots = _read_plots(server["db_url"])
        matching = [
            p for p in plots if p.name == "same_plot" and p.grimoire_name == "g_replace"
        ]
        assert len(matching) == 1
        stored = json.loads(matching[0].json_data)
        assert stored["layout"]["title"]["text"] == "Replacement"


class TestAuthentication:
    """Tests for authentication enforcement."""

    def test_missing_secret_returns_401(self, server):
        """Request without grimoire-secret header should return 401."""
        resp = requests.post(
            f"{server['url']}/add_plot",
            json={
                "grimoire_name": "g1",
                "chapter_name": "ch1",
                "plot_name": "p1",
                "json_data": "{}",
            },
        )
        assert resp.status_code == 401

    def test_wrong_secret_returns_403(self, server):
        """Request with wrong secret should return 403."""
        resp = requests.post(
            f"{server['url']}/add_plot",
            headers={"grimoire-secret": "wrong-secret"},
            json={
                "grimoire_name": "auth_fail",
                "chapter_name": "ch1",
                "plot_name": "p1",
                "json_data": "{}",
            },
        )
        assert resp.status_code == 403

        # DB should not have this grimoire
        plots = _read_plots(server["db_url"])
        assert not any(p.grimoire_name == "auth_fail" for p in plots)


class TestDeleteEndpoints:
    """Tests for delete endpoints."""

    def _push_plot(self, server, grimoire="g_del", chapter="ch_del", plot="p_del"):
        fig = _make_figure("delete test")
        resp = requests.post(
            f"{server['url']}/add_plot",
            headers={"grimoire-secret": server["secret"]},
            json={
                "grimoire_name": grimoire,
                "chapter_name": chapter,
                "plot_name": plot,
                "json_data": fig.to_json(),
            },
        )
        assert resp.status_code == 200

    def test_delete_plot(self, server):
        """Delete a specific plot and verify it's gone."""
        self._push_plot(server, grimoire="gd1", chapter="cd1", plot="pd1")

        resp = requests.delete(
            f"{server['url']}/grimoire/gd1/chapter/cd1/plot/pd1",
            headers={"grimoire-secret": server["secret"]},
        )
        assert resp.status_code == 200

        plots = _read_plots(server["db_url"])
        assert not any(p.name == "pd1" and p.grimoire_name == "gd1" for p in plots)

    def test_delete_chapter(self, server):
        """Delete a chapter and verify it and its plots are gone."""
        self._push_plot(server, grimoire="gd2", chapter="cd2", plot="pd2a")
        self._push_plot(server, grimoire="gd2", chapter="cd2", plot="pd2b")

        resp = requests.delete(
            f"{server['url']}/grimoire/gd2/chapter/cd2",
            headers={"grimoire-secret": server["secret"]},
        )
        assert resp.status_code == 200

        chapters = _read_chapters(server["db_url"])
        assert not any(c.name == "cd2" and c.grimoire_name == "gd2" for c in chapters)
        plots = _read_plots(server["db_url"])
        assert not any(p.grimoire_name == "gd2" for p in plots)

    def test_delete_grimoire(self, server):
        """Delete a grimoire and verify everything under it is gone."""
        self._push_plot(server, grimoire="gd3", chapter="cd3", plot="pd3")

        resp = requests.delete(
            f"{server['url']}/grimoire/gd3",
            headers={"grimoire-secret": server["secret"]},
        )
        assert resp.status_code == 200

        grimoires = _read_grimoires(server["db_url"])
        assert not any(g.name == "gd3" for g in grimoires)

    def test_delete_nonexistent_returns_404(self, server):
        """Deleting something that doesn't exist should return 404."""
        resp = requests.delete(
            f"{server['url']}/grimoire/nope",
            headers={"grimoire-secret": server["secret"]},
        )
        assert resp.status_code == 404


class TestClientIntegration:
    """Test using the actual client functions to push plots."""

    def test_push_plot_sync(self, server):
        """Use the client's push_plot_sync function."""
        from grimoireplot.client import push_plot_sync

        fig = _make_figure("Client Test")
        result = push_plot_sync(
            grimoire_name="client_g",
            chapter_name="client_ch",
            plot_name="client_p",
            fig=fig,
            grimoire_secret=server["secret"],
            grimoire_server=server["url"],
        )
        assert result["status"] == "success"

        plots = _read_plots(server["db_url"])
        matching = [
            p for p in plots if p.name == "client_p" and p.grimoire_name == "client_g"
        ]
        assert len(matching) == 1
        assert matching[0].chapter_name == "client_ch"
