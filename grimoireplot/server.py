from fastapi import HTTPException, Request
from nicegui import app, ui
from grimoireplot.client import get_grimoire_server
from grimoireplot.common import get_grimoire_secret
from grimoireplot.models import (
    AddPlotRequest,
    create_db_and_tables,
    add_plot,
    delete_plot,
    delete_chapter,
    delete_grimoire,
)

from grimoireplot.ui import dashboard_ui

_GRIMOIRE_SECRET = get_grimoire_secret()
_GRIMOIRE_SERVER = get_grimoire_server()


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
        dashboard_ui.refresh()  # Refresh the dashboard to show the new plot
        return {"status": "success", "plot_name": plot.name}

    @app.delete("/plot/{plot_name}")
    def delete_plot_endpoint(plot_name: str, request: Request):
        verify_secret(request)
        if not delete_plot(plot_name):
            raise HTTPException(status_code=404, detail="Plot not found")
        dashboard_ui.refresh()
        return {"status": "success", "deleted": plot_name}

    @app.delete("/chapter/{chapter_name}")
    def delete_chapter_endpoint(chapter_name: str, request: Request):
        verify_secret(request)
        if not delete_chapter(chapter_name):
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
        dashboard_ui()

    host, port = _GRIMOIRE_SERVER.split("://")[-1].split(":")
    ui.run(host=host, port=int(port))
