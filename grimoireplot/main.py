"""
Main CLI for GrimoirePlot application.
"""

import argparse
from grimoireplot.common import get_grimoire_secret, get_grimoire_server


def serve_command(args):
    """Run the GrimoirePlot server."""
    from grimoireplot.server import my_app

    my_app(host=args.host, port=args.port)


def push_samples_command(args):
    """Push sample plots to test the server."""
    from grimoireplot.client import push_plot_sync
    from grimoireplot.create_some_plots import (
        create_sample_line_plot,
        create_sample_bar_plot,
        create_sample_scatter_plot,
        create_sample_histogram,
        create_sample_pie_chart,
        create_sample_box_plot,
        create_sample_heatmap,
        create_sample_area_plot,
    )

    server_url = f"http://{args.host}:{args.port}"
    grimoire_name = args.grimoire_name

    samples = [
        ("Basic Plots", "Line Plot", create_sample_line_plot),
        ("Basic Plots", "Bar Plot", create_sample_bar_plot),
        ("Basic Plots", "Area Plot", create_sample_area_plot),
        ("Distributions", "Scatter Plot", create_sample_scatter_plot),
        ("Distributions", "Histogram", create_sample_histogram),
        ("Distributions", "Box Plot", create_sample_box_plot),
        ("Categories", "Pie Chart", create_sample_pie_chart),
        ("Categories", "Heatmap", create_sample_heatmap),
    ]

    print(f"Pushing {len(samples)} sample plots to {server_url}")
    print(f"Grimoire: {grimoire_name}")
    print("-" * 40)

    for chapter, plot_name, create_func in samples:
        try:
            fig = create_func()
            _ = push_plot_sync(
                grimoire_name=grimoire_name,
                chapter_name=chapter,
                plot_name=plot_name,
                fig=fig,
                grimoire_secret=args.secret,
                grimoire_server=server_url,
            )
            print(f"  [OK] {chapter}/{plot_name}")
        except Exception as e:
            print(f"  [FAIL] {chapter}/{plot_name}: {e}")

    print("-" * 40)
    print("Done!")


def main():
    default_server = get_grimoire_server()
    default_host = default_server.split("://")[-1].split(":")[0]
    default_port = int(default_server.split(":")[-1])
    default_secret = get_grimoire_secret()

    parser = argparse.ArgumentParser(
        prog="grimoireplot",
        description="GrimoirePlot - Live dashboard for Plotly-compatible plots",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the GrimoirePlot server")
    serve_parser.add_argument(
        "--host",
        type=str,
        default=default_host,
        help=f"Host to bind the server (default: {default_host})",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help=f"Port to bind the server (default: {default_port})",
    )
    serve_parser.set_defaults(func=serve_command)

    # Push samples command
    push_parser = subparsers.add_parser(
        "push-samples", help="Push sample plots to test the server"
    )
    push_parser.add_argument(
        "--host",
        type=str,
        default=default_host,
        help=f"Server host (default: {default_host})",
    )
    push_parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help=f"Server port (default: {default_port})",
    )
    push_parser.add_argument(
        "--secret",
        type=str,
        default=default_secret,
        help="Grimoire secret for authentication",
    )
    push_parser.add_argument(
        "--grimoire-name",
        type=str,
        default="test_grimoire",
        help="Name of the grimoire to create (default: test_grimoire)",
    )
    push_parser.set_defaults(func=push_samples_command)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ in {"__main__", "__mp_main__"}:
    main()
