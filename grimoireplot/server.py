import random
from nicegui import app, ui
from grimoireplot.models import create_db_and_tables


def my_app():
    create_db_and_tables()

    @app.get("/random/{max}")
    def generate_random_number(max: int):
        return {"min": 0, "max": max, "value": random.randint(0, max)}

    @ui.page("/")
    def page():
        max = ui.number("max", value=100)
        ui.button(
            "generate random number",
            on_click=lambda: ui.navigate.to(f"/random/{max.value:.0f}"),
        )

    ui.run()
