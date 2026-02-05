"""
Client module that push plots
"""

from plotly.graph_objects import Figure
import aiohttp
import requests
from grimoireplot.common import get_grimoire_secret, get_grimoire_server


default_secret = get_grimoire_secret()
default_server = get_grimoire_server()


def push_plot_sync(
    grimoire_name: str,
    chapter_name: str,
    plot_name: str,
    fig: Figure,
    grimoire_secret: str = default_secret,
    grimoire_server: str = default_server,
) -> dict:
    """Push a plot to the grimoire server.

    Args:
        grimoire_name (str): Name of the grimoire.
        chapter_name (str): Name of the chapter.
        plot_name (str): Name of the plot.
        fig (Figure): Plotly figure to push.
        grimoire_secret (str, optional): Secret for authentication. Defaults to default_secret.
        grimoire_server (str, optional): Grimoire server URL. Defaults to default_server.

    Returns:
        dict: Response from the server.
    """
    json_data = fig.to_json()
    match json_data:
        case str():
            return push_plot_json_sync(
                grimoire_name=grimoire_name,
                chapter_name=chapter_name,
                plot_name=plot_name,
                json_data=json_data,
                grimoire_secret=grimoire_secret,
                grimoire_server=grimoire_server,
            )
        case _:
            raise ValueError(
                "fig.to_json() did not return a string, maybe fig is invalid?"
            )


def push_plot_json_sync(
    grimoire_name: str,
    chapter_name: str,
    plot_name: str,
    json_data: str,
    grimoire_secret: str = default_secret,
    grimoire_server: str = default_server,
) -> dict:
    """Push a plot to the grimoire server.

    Args:
        grimoire_name (str): Name of the grimoire.
        chapter_name (str): Name of the chapter.
        plot_name (str): Name of the plot.
        json_data (str): JSON representation of the plotly figure.
        grimoire_secret (str, optional): Secret for authentication. Defaults to default_secret.
        grimoire_server (str, optional): Grimoire server URL. Defaults to defualt_server.

    Returns:
        dict: Response from the server.
    """

    url = f"{grimoire_server}/add_plot"
    headers = {"grimoire-secret": grimoire_secret}

    payload = {
        "grimoire_name": grimoire_name,
        "chapter_name": chapter_name,
        "plot_name": plot_name,
        "json_data": json_data,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


async def push_plot(
    grimoire_name: str,
    chapter_name: str,
    plot_name: str,
    fig: Figure,
    grimoire_secret: str = default_secret,
    grimoire_server: str = default_server,
) -> dict:
    """Push a plot to the grimoire server asynchronously.

    Args:
        grimoire_name (str): Name of the grimoire.
        chapter_name (str): Name of the chapter.
        plot_name (str): Name of the plot.
        fig (Figure): Plotly figure to push.
        grimoire_secret (str, optional): Secret for authentication. Defaults to default_secret.
        grimoire_server (str, optional): Grimoire server URL. Defaults to default_server.

    Returns:
        dict: Response from the server.
    """
    json_data = fig.to_json()
    match json_data:
        case str():
            return await push_plot_json(
                grimoire_name=grimoire_name,
                chapter_name=chapter_name,
                plot_name=plot_name,
                json_data=json_data,
                grimoire_secret=grimoire_secret,
                grimoire_server=grimoire_server,
            )
        case _:
            raise ValueError(
                "fig.to_json() did not return a string, maybe fig is invalid?"
            )


async def push_plot_json(
    grimoire_name: str,
    chapter_name: str,
    plot_name: str,
    json_data: str,
    grimoire_secret: str = default_secret,
    grimoire_server: str = default_server,
) -> dict:
    """Push a plot to the grimoire server asynchronously.

    Args:
        grimoire_name (str): Name of the grimoire.
        chapter_name (str): Name of the chapter.
        plot_name (str): Name of the plot.
        json_data (str): JSON representation of the plotly figure.
        grimoire_secret (str, optional): Secret for authentication. Defaults to default_secret.
        grimoire_server (str, optional): Grimoire server URL. Defaults to default_server.

    Returns:
        dict: Response from the server.
    """
    url = f"{grimoire_server}/add_plot"
    headers = {"grimoire-secret": grimoire_secret}

    payload = {
        "grimoire_name": grimoire_name,
        "chapter_name": chapter_name,
        "plot_name": plot_name,
        "json_data": json_data,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return await response.json()
