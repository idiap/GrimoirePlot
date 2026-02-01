from dotenv import load_dotenv
from fastapi import HTTPException, Request
from nicegui import app, ui
from grimoireplot.models import AddPlotRequest, create_db_and_tables, add_plot
import os
from loguru import logger

from grimoireplot.ui import DashboardUI

load_dotenv()

if (_GRIMOIRE_SECRET := os.environ.get("GRIMOIRE_SECRET")) is None:
    logger.warning("GRIMOIRE_SECRET not set; using default secret")
    _GRIMOIRE_SECRET = "IDidntSetASecret"


def verify_secret(request: Request):
    if (secret := request.headers.get("grimoire-secret")) is None:
        raise HTTPException(status_code=401, detail="grimoire-secret not found")
    if secret != _GRIMOIRE_SECRET:
        raise HTTPException(status_code=403, detail="invalid grimoire-secret")


def my_app():
    create_db_and_tables()

    @app.post("/add_plot")
    def add_plot_endpoint(add_plot_request: AddPlotRequest, request: Request):
        verify_secret(request)
        plot = add_plot(
            grimoire_name=add_plot_request.grimoire_name,
            chapter_name=add_plot_request.chapter_name,
            plot_name=add_plot_request.plot_name,
            json_data=add_plot_request.json_data,
        )
        return {"status": "success", "plot_name": plot.name}

    @ui.page("/")
    def page():
        DashboardUI()

    ui.run()
