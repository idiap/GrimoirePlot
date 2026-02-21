# GrimoirePlot

*GrimoirePlot is a live dashboard of plotly-compatible plots of remote data*

![demo](media/demo_grimoire.gif)

## Adding to your current project

```bash
uv add grimoireplot
```

Or install from source:

```bash
# git clone the repo
cd grimoireplot
uv sync --extra dev
```

### Installation as a tool

```bash
uv tool install grimoireplot  # not yet on pypi, will setup ci/cd on github later on
```

## Quick Start

### 1. Start the Server

```bash
grimoireplot serve --host localhost --port 8080
```

Then open your browser at `http://localhost:8080` to see the dashboard.

### 2. Push Sample Plots (Test the Server)

In another terminal, push some sample plots to verify everything works:

```bash
grimoireplot push-samples --host localhost --port 8080
```

## CLI Reference

### `grimoireplot serve`

Start the GrimoirePlot dashboard server.

```bash
grimoireplot serve [--host HOST] [--port PORT]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `localhost` | Host to bind the server |
| `--port` | `8080` | Port to bind the server |

### `grimoireplot push-samples`

Push sample plots to test the server.

```bash
grimoireplot push-samples [--host HOST] [--port PORT] [--secret SECRET] [--grimoire-name NAME]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `localhost` | Server host |
| `--port` | `8080` | Server port |
| `--secret` | `IDidntSetASecret` | Authentication secret |
| `--grimoire-name` | `test_grimoire` | Name of the grimoire to create |

### `grimoireplot live-test`

Test live plot updates by continuously adding datapoints to a line plot.

```bash
grimoireplot live-test [--host HOST] [--port PORT] [--secret SECRET] [--grimoire-name NAME] [--interval SECONDS] [--max-points N]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `localhost` | Server host |
| `--port` | `8080` | Server port |
| `--secret` | `IDidntSetASecret` | Authentication secret |
| `--grimoire-name` | `live_test` | Name of the grimoire to create |
| `--interval` | `0.2` | Interval between datapoints in seconds |
| `--max-points` | `0` | Maximum number of points (0 = unlimited) |

## Programmatic Usage

### Sending Plots from Python

GrimoirePlot organizes plots in a hierarchy: **Grimoire** → **Chapter** → **Plot**

#### Synchronous API

```python
import plotly.graph_objects as go
from grimoireplot.client import push_plot_sync

# Create a Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines+markers'))
fig.update_layout(title='My Plot')

# Push to the server
response = push_plot_sync(
    grimoire_name="my_experiment",
    chapter_name="training_metrics",
    plot_name="loss_curve",
    fig=fig,
    grimoire_server="http://localhost:8080",
    grimoire_secret="your-secret",
)
```

#### Asynchronous API

```python
import asyncio
import plotly.graph_objects as go
from grimoireplot.client import push_plot

async def main():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[20, 14, 23]))
    fig.update_layout(title='Async Plot')

    response = await push_plot(
        grimoire_name="my_experiment",
        chapter_name="results",
        plot_name="bar_chart",
        fig=fig,
        grimoire_server="http://localhost:8080",
        grimoire_secret="your-secret",
    )

asyncio.run(main())
```

### Integration Example: Training Loop

```python
import plotly.graph_objects as go
from grimoireplot.client import push_plot_sync

losses = []

for epoch in range(100):
    loss = train_one_epoch()  # Your training code
    losses.append(loss)

    # Update the plot every 10 epochs
    if epoch % 10 == 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=losses, mode='lines', name='Training Loss'))
        fig.update_layout(title=f'Training Progress (Epoch {epoch})',
                          xaxis_title='Epoch', yaxis_title='Loss')

        push_plot_sync(
            grimoire_name="experiment_001",
            chapter_name="training",
            plot_name="loss",
            fig=fig,
        )
```

## Configuration

GrimoirePlot can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GRIMOIRE_SERVER` | `http://localhost:8080` | Default server URL |
| `GRIMOIRE_SECRET` | `IDidntSetASecret` | Authentication secret |

You can also use a `.env` file in your project directory.

## Testing

```bash
# you need to install with --extra dev
GRIMOIRE_TEST=true uv run pytest
```

## Concepts

- **Grimoire**: A collection of related visualizations (e.g., an experiment)
- **Chapter**: A group of plots within a grimoire (e.g., training metrics, evaluation results)
- **Plot**: A single Plotly figure

## Acknowledgments

GrimoirePlot is inspired by [visdom](https://github.com/fossasia/visdom)
