"""module for nicegui UI components"""

from nicegui import ui


class DashboardUI:
    """Top level component"""

    def __init__(self):
        self.grimoires = []
        with ui.tabs().classes("w-full") as tabs:
            tab1 = ui.tab("Grimoire One")
            tab2 = ui.tab("Grimoire Two")
        with ui.tab_panels(tabs, value=tab1).classes("w-full"):
            with ui.tab_panel(tab1):
                grimoire1 = GrimoireUI("Grimoire One")
                self.grimoires.append(grimoire1)
            with ui.tab_panel(tab2):
                grimoire2 = GrimoireUI("Grimoire Two")
                self.grimoires.append(grimoire2)


class GrimoireUI:
    """Grimoire UI component"""

    def __init__(self, name: str):
        self.name = name
        self.chapters = []
        with ui.tabs().classes("w-full") as tabs:
            tab1 = ui.tab("One")
            tab2 = ui.tab("Two")
        with ui.tab_panels(tabs, value=tab1).classes("w-full"):
            with ui.tab_panel(tab1):
                ch1 = ChapterUI("One")
                self.chapters.append(ch1)
            with ui.tab_panel(tab2):
                ch2 = ChapterUI("Two")
                self.chapters.append(ch2)


class ChapterUI:
    """Chapter UI component"""

    def __init__(self, name: str):
        self.name = name
        self.plots = []
        with ui.grid(columns=6).classes("w-full gap-2 p-2"):
            for _ in range(30):
                current_plot = PlotUI()
                self.plots.append(current_plot)


class PlotUI:
    """Plot UI component"""

    def __init__(self):
        fig = {
            "data": [
                {
                    "type": "scatter",
                    "name": "Trace 1",
                    "x": [1, 2, 3, 4],
                    "y": [1, 2, 3, 2.5],
                },
                {
                    "type": "scatter",
                    "name": "Trace 2",
                    "x": [1, 2, 3, 4],
                    "y": [1.4, 1.8, 3.8, 3.2],
                    "line": {"dash": "dot", "width": 3},
                },
            ],
            "layout": {
                "margin": {"l": 15, "r": 0, "t": 0, "b": 15},
                "plot_bgcolor": "#E5ECF6",
                "xaxis": {"gridcolor": "white"},
                "yaxis": {"gridcolor": "white"},
            },
        }
        self.plot = ui.plotly(fig).classes("w-full h-40")
