# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

import time
import logging
from functools import wraps

from fastapi import HTTPException, Request
from nicegui import app, ui
from grimoireplot.common import get_grimoire_secret
from grimoireplot.models import (
    AddPlotRequest,
    create_db_and_tables,
    add_plot,
    delete_plot,
    delete_chapter,
    delete_grimoire,
)

from grimoireplot.ui import dashboard_ui, refresh_chapter_plots
from grimoireplot.ui_elements import setup_theme

_GRIMOIRE_SECRET = get_grimoire_secret()

logger = logging.getLogger("grimoireplot")


def retry_on_db_error(max_retries: int = 5, base_delay: float = 0.1):
    """Decorator that retries a function on database errors up to max_retries times."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except HTTPException:
                    raise
                except Exception as e:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        logger.warning(
                            "Database error on attempt %d/%d: %s. Retrying in %.2fs...",
                            attempt,
                            max_retries,
                            str(e),
                            delay,
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            "Database error on attempt %d/%d: %s. No more retries.",
                            attempt,
                            max_retries,
                            str(e),
                        )
                        raise

        return wrapper

    return decorator


def verify_secret(request: Request):
    if (secret := request.headers.get("grimoire-secret")) is None:
        raise HTTPException(status_code=401, detail="grimoire-secret not found")
    if secret != _GRIMOIRE_SECRET:
        raise HTTPException(status_code=403, detail="invalid grimoire-secret")


def my_app(host: str = "localhost", port: int = 8080):
    create_db_and_tables()

    @app.post("/add_plot")
    @retry_on_db_error(max_retries=5)
    def add_plot_endpoint(add_plot_request: AddPlotRequest, request: Request):
        verify_secret(request)
        plot = add_plot(
            grimoire_name=add_plot_request.grimoire_name,
            chapter_name=add_plot_request.chapter_name,
            plot_name=add_plot_request.plot_name,
            json_data=add_plot_request.json_data,
        )
        # Try to refresh only the specific chapter's plots
        # If the chapter doesn't exist in UI yet (new grimoire/chapter), refresh the whole dashboard
        if not refresh_chapter_plots(
            add_plot_request.grimoire_name, add_plot_request.chapter_name
        ):
            dashboard_ui.refresh()
        return {"status": "success", "plot_name": plot.name}

    @app.delete("/grimoire/{grimoire_name}/chapter/{chapter_name}/plot/{plot_name}")
    def delete_plot_endpoint(
        grimoire_name: str, chapter_name: str, plot_name: str, request: Request
    ):
        verify_secret(request)
        if not delete_plot(grimoire_name, chapter_name, plot_name):
            raise HTTPException(status_code=404, detail="Plot not found")
        dashboard_ui.refresh()
        return {"status": "success", "deleted": plot_name}

    @app.delete("/grimoire/{grimoire_name}/chapter/{chapter_name}")
    def delete_chapter_endpoint(
        grimoire_name: str, chapter_name: str, request: Request
    ):
        verify_secret(request)
        if not delete_chapter(grimoire_name, chapter_name):
            raise HTTPException(status_code=404, detail="Chapter not found")
        dashboard_ui.refresh()
        return {"status": "success", "deleted": chapter_name}

    @app.delete("/grimoire/{grimoire_name}")
    def delete_grimoire_endpoint(grimoire_name: str, request: Request):
        verify_secret(request)
        if not delete_grimoire(grimoire_name):
            raise HTTPException(status_code=404, detail="Grimoire not found")
        dashboard_ui.refresh()
        return {"status": "success", "deleted": grimoire_name}

    @ui.page("/")
    def page():
        setup_theme()
        dashboard_ui()

    ui.run(
        host=host,
        port=port,
        dark=True,
        title="GrimoirePlot - Data Visualization Dashboard",
        favicon="🔮",
        reload=False,
    )
