"""
Main CLI for GrimoirePlot application.
"""

import argparse
from grimoireplot.common import get_grimoire_secret, get_grimoire_server


def serve_command(args):
    """Run the GrimoirePlot server."""
    from grimoireplot.server import my_app

    my_app(host=args.host, port=args.port)


def live_test_command(args):
    """Run a live test that adds one datapoint every 0.2 seconds to two plots."""
    import time
    import math
    import plotly.graph_objects as go
    from grimoireplot.client import push_plot_sync

    server_url = f"http://{args.host}:{args.port}"
    grimoire_name = args.grimoire_name
    chapter_name = "Live Test"

    print(f"Starting live test to {server_url}")
    print(f"Grimoire: {grimoire_name}")
    print(f"Adding one datapoint every {args.interval} seconds to 2 plots")
    print("Press Ctrl+C to stop")
    print("-" * 40)

    # Data for plot 1 (sine wave)
    x_data_1 = []
    y_data_1 = []
    # Data for plot 2 (cosine wave)
    x_data_2 = []
    y_data_2 = []
    step = 0

    try:
        while args.max_points == 0 or step < args.max_points:
            # Generate new datapoints
            x_data_1.append(step)
            y_data_1.append(math.sin(step * 0.1) + (step * 0.01))
            x_data_2.append(step)
            y_data_2.append(math.cos(step * 0.1) + (step * 0.01))

            # Create figure 1 (sine wave)
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=x_data_1,
                    y=y_data_1,
                    mode="lines+markers",
                    name="Sine Wave",
                    line=dict(color="blue"),
                    marker=dict(size=6),
                )
            )
            fig1.update_layout(
                title=f"Sine Wave (Point {step + 1})",
                xaxis_title="Step",
                yaxis_title="Value",
            )

            # Create figure 2 (cosine wave)
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=x_data_2,
                    y=y_data_2,
                    mode="lines+markers",
                    name="Cosine Wave",
                    line=dict(color="red"),
                    marker=dict(size=6),
                )
            )
            fig2.update_layout(
                title=f"Cosine Wave (Point {step + 1})",
                xaxis_title="Step",
                yaxis_title="Value",
            )

            # Push both plots to server
            try:
                push_plot_sync(
                    grimoire_name=grimoire_name,
                    chapter_name=chapter_name,
                    plot_name="Sine Wave",
                    fig=fig1,
                    grimoire_secret=args.secret,
                    grimoire_server=server_url,
                )
                push_plot_sync(
                    grimoire_name=grimoire_name,
                    chapter_name=chapter_name,
                    plot_name="Cosine Wave",
                    fig=fig2,
                    grimoire_secret=args.secret,
                    grimoire_server=server_url,
                )
                print(
                    f"  Point {step + 1}: sin={y_data_1[-1]:.4f}, cos={y_data_2[-1]:.4f}"
                )
            except Exception as e:
                print(f"  [ERROR] Failed to push point {step + 1}: {e}")

            step += 1
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n" + "-" * 40)
        print(f"Stopped after {step} points")

    print("Done!")


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

    # Live test command
    live_parser = subparsers.add_parser(
        "live-test", help="Test live plot updates by adding datapoints over time"
    )
    live_parser.add_argument(
        "--host",
        type=str,
        default=default_host,
        help=f"Server host (default: {default_host})",
    )
    live_parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help=f"Server port (default: {default_port})",
    )
    live_parser.add_argument(
        "--secret",
        type=str,
        default=default_secret,
        help="Grimoire secret for authentication",
    )
    live_parser.add_argument(
        "--grimoire-name",
        type=str,
        default="live_test",
        help="Name of the grimoire to create (default: live_test)",
    )
    live_parser.add_argument(
        "--interval",
        type=float,
        default=0.2,
        help="Interval between datapoints in seconds (default: 0.2)",
    )
    live_parser.add_argument(
        "--max-points",
        type=int,
        default=0,
        help="Maximum number of points to add (0 = unlimited, default: 0)",
    )
    live_parser.set_defaults(func=live_test_command)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ in {"__main__", "__mp_main__"}:
    main()
