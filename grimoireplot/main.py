"""
Main for GrimoirePlot application.
"""

from grimoireplot.server import my_app


def main():
    my_app()


if __name__ in {"__main__", "__mp_main__"}:
    main()
