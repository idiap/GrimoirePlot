"""
Script to manually test the grimoire server by pushing some sample plots.
"""

import plotly.graph_objects as go
from grimoireplot.client import push_plot_sync


def create_sample_line_plot():
    """Create a simple line plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode="lines+markers", name="Line 1"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3, 4], y=[16, 15, 14, 13], mode="lines+markers", name="Line 2"
        )
    )
    fig.update_layout(
        title="Sample Line Plot", xaxis_title="X Axis", yaxis_title="Y Axis"
    )
    return fig


def create_sample_bar_plot():
    """Create a simple bar plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Category A", "Category B", "Category C"],
            y=[20, 14, 23],
            name="Series 1",
        )
    )
    fig.add_trace(
        go.Bar(
            x=["Category A", "Category B", "Category C"],
            y=[12, 18, 29],
            name="Series 2",
        )
    )
    fig.update_layout(
        title="Sample Bar Plot", xaxis_title="Categories", yaxis_title="Values"
    )
    return fig


def create_sample_scatter_plot():
    """Create a simple scatter plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[1, 4, 9, 16, 25],
            mode="markers",
            marker=dict(size=10, color="blue"),
            name="Quadratic",
        )
    )
    fig.update_layout(title="Sample Scatter Plot", xaxis_title="X", yaxis_title="Y")
    return fig


def create_sample_histogram():
    """Create a simple histogram."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=[1, 1, 2, 3, 3, 3, 4, 4, 5], name="Data"))
    fig.update_layout(
        title="Sample Histogram", xaxis_title="Value", yaxis_title="Frequency"
    )
    return fig


def create_sample_pie_chart():
    """Create a simple pie chart."""
    fig = go.Figure()
    fig.add_trace(
        go.Pie(labels=["A", "B", "C", "D"], values=[15, 30, 45, 10], name="Pie")
    )
    fig.update_layout(title="Sample Pie Chart")
    return fig


def create_sample_box_plot():
    """Create a simple box plot."""
    fig = go.Figure()
    fig.add_trace(go.Box(y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], name="Box 1"))
    fig.add_trace(go.Box(y=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11], name="Box 2"))
    fig.update_layout(title="Sample Box Plot", yaxis_title="Values")
    return fig


def create_sample_heatmap():
    """Create a simple heatmap."""
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], x=["A", "B", "C"], y=["X", "Y", "Z"]
        )
    )
    fig.update_layout(title="Sample Heatmap")
    return fig


def create_sample_3d_scatter():
    """Create a simple 3D scatter plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=[1, 2, 3, 4],
            y=[5, 6, 7, 8],
            z=[9, 10, 11, 12],
            mode="markers",
            name="3D Points",
        )
    )
    fig.update_layout(title="Sample 3D Scatter Plot")
    return fig


def create_sample_area_plot():
    """Create a simple area plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill="tozeroy", name="Area 1")
    )
    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill="tonexty", name="Area 2")
    )
    fig.update_layout(title="Sample Area Plot", xaxis_title="X", yaxis_title="Y")
    return fig


def create_sample_violin_plot():
    """Create a simple violin plot."""
    fig = go.Figure()
    fig.add_trace(go.Violin(y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], name="Violin 1"))
    fig.add_trace(go.Violin(y=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11], name="Violin 2"))
    fig.update_layout(title="Sample Violin Plot", yaxis_title="Values")
    return fig


def create_sample_contour_plot():
    """Create a simple contour plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Contour(
            z=[
                [10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5.0, 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10],
            ],
            name="Contour",
        )
    )
    fig.update_layout(title="Sample Contour Plot")
    return fig


def create_sample_surface_plot():
    """Create a simple 3D surface plot."""
    fig = go.Figure()
    fig.add_trace(go.Surface(z=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], name="Surface"))
    fig.update_layout(title="Sample Surface Plot")
    return fig


def create_sample_waterfall():
    """Create a simple waterfall plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Waterfall(
            x=["Start", "A", "B", "C", "Total"],
            y=[0, 10, -5, 8, 0],
            measure=["absolute", "relative", "relative", "relative", "total"],
            name="Waterfall",
        )
    )
    fig.update_layout(title="Sample Waterfall Plot")
    return fig


def create_sample_funnel():
    """Create a simple funnel plot."""
    fig = go.Figure()
    fig.add_trace(
        go.Funnel(
            y=["Stage 1", "Stage 2", "Stage 3", "Stage 4"],
            x=[100, 80, 60, 40],
            name="Funnel",
        )
    )
    fig.update_layout(title="Sample Funnel Plot")
    return fig


if __name__ == "__main__":
    grimoires = [
        "test_grimoire",
        "analysis_grimoire",
        "dashboard_grimoire",
        "extra_grimoire",
    ]

    for grimoire_name in grimoires:
        print(f"\n--- Pushing plots to {grimoire_name} ---")

        # Chapter 1: Basic plots (3 plots)
        print("Pushing line plot...")
        line_fig = create_sample_line_plot()
        response = push_plot_sync(grimoire_name, "Chapter 1", "Line Plot", line_fig)
        print(f"Response: {response}")

        print("Pushing bar plot...")
        bar_fig = create_sample_bar_plot()
        response = push_plot_sync(grimoire_name, "Chapter 1", "Bar Plot", bar_fig)
        print(f"Response: {response}")

        print("Pushing area plot...")
        area_fig = create_sample_area_plot()
        response = push_plot_sync(grimoire_name, "Chapter 1", "Area Plot", area_fig)
        print(f"Response: {response}")

        # Chapter 2: Scatter and distribution (3 plots)
        print("Pushing scatter plot...")
        scatter_fig = create_sample_scatter_plot()
        response = push_plot_sync(
            grimoire_name, "Chapter 2", "Scatter Plot", scatter_fig
        )
        print(f"Response: {response}")

        print("Pushing histogram...")
        hist_fig = create_sample_histogram()
        response = push_plot_sync(grimoire_name, "Chapter 2", "Histogram", hist_fig)
        print(f"Response: {response}")

        print("Pushing violin plot...")
        violin_fig = create_sample_violin_plot()
        response = push_plot_sync(grimoire_name, "Chapter 2", "Violin Plot", violin_fig)
        print(f"Response: {response}")

        # Chapter 3: Categorical (2 plots)
        print("Pushing pie chart...")
        pie_fig = create_sample_pie_chart()
        response = push_plot_sync(grimoire_name, "Chapter 3", "Pie Chart", pie_fig)
        print(f"Response: {response}")

        print("Pushing box plot...")
        box_fig = create_sample_box_plot()
        response = push_plot_sync(grimoire_name, "Chapter 3", "Box Plot", box_fig)
        print(f"Response: {response}")

        # Chapter 4: Matrix and contours (2 plots)
        print("Pushing heatmap...")
        heat_fig = create_sample_heatmap()
        response = push_plot_sync(grimoire_name, "Chapter 4", "Heatmap", heat_fig)
        print(f"Response: {response}")

        print("Pushing contour plot...")
        contour_fig = create_sample_contour_plot()
        response = push_plot_sync(
            grimoire_name, "Chapter 4", "Contour Plot", contour_fig
        )
        print(f"Response: {response}")

        # Chapter 5: 3D visualizations (2 plots)
        print("Pushing 3D scatter plot...")
        scatter3d_fig = create_sample_3d_scatter()
        response = push_plot_sync(
            grimoire_name, "Chapter 5", "3D Scatter", scatter3d_fig
        )
        print(f"Response: {response}")

        print("Pushing surface plot...")
        surface_fig = create_sample_surface_plot()
        response = push_plot_sync(
            grimoire_name, "Chapter 5", "Surface Plot", surface_fig
        )
        print(f"Response: {response}")

        # Chapter 6: Specialized plots (2 plots)
        print("Pushing waterfall plot...")
        waterfall_fig = create_sample_waterfall()
        response = push_plot_sync(
            grimoire_name, "Chapter 6", "Waterfall Plot", waterfall_fig
        )
        print(f"Response: {response}")

        print("Pushing funnel plot...")
        funnel_fig = create_sample_funnel()
        response = push_plot_sync(grimoire_name, "Chapter 6", "Funnel Plot", funnel_fig)
        print(f"Response: {response}")

        # Chapter 7: Additional basic plots (2 plots)
        print("Pushing additional line plot...")
        line_fig2 = create_sample_line_plot()
        line_fig2.update_layout(title="Additional Line Plot")
        response = push_plot_sync(
            grimoire_name, "Chapter 7", "Additional Line", line_fig2
        )
        print(f"Response: {response}")

        print("Pushing additional bar plot...")
        bar_fig2 = create_sample_bar_plot()
        bar_fig2.update_layout(title="Additional Bar Plot")
        response = push_plot_sync(
            grimoire_name, "Chapter 7", "Additional Bar", bar_fig2
        )
        print(f"Response: {response}")

        # Chapter 8: More distribution plots (2 plots)
        print("Pushing additional histogram...")
        hist_fig2 = create_sample_histogram()
        hist_fig2.update_layout(title="Additional Histogram")
        response = push_plot_sync(
            grimoire_name, "Chapter 8", "Additional Histogram", hist_fig2
        )
        print(f"Response: {response}")

        print("Pushing additional box plot...")
        box_fig2 = create_sample_box_plot()
        box_fig2.update_layout(title="Additional Box Plot")
        response = push_plot_sync(
            grimoire_name, "Chapter 8", "Additional Box", box_fig2
        )
        print(f"Response: {response}")

        # Chapter 9: Final visualizations (2 plots)
        print("Pushing additional scatter plot...")
        scatter_fig2 = create_sample_scatter_plot()
        scatter_fig2.update_layout(title="Additional Scatter Plot")
        response = push_plot_sync(
            grimoire_name, "Chapter 9", "Additional Scatter", scatter_fig2
        )
        print(f"Response: {response}")

        print("Pushing additional pie chart...")
        pie_fig2 = create_sample_pie_chart()
        pie_fig2.update_layout(title="Additional Pie Chart")
        response = push_plot_sync(
            grimoire_name, "Chapter 9", "Additional Pie", pie_fig2
        )
        print(f"Response: {response}")
