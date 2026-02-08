"""
Styled UI components for GrimoirePlot.

This module provides factory functions for creating consistently styled UI elements.
All appearance customization is centralized here for easy theming.
"""

from typing import Callable, Any, Optional
from nicegui import ui

# ============================================================================
# THEME CONFIGURATION
# ============================================================================

# Color palette - mystical/grimoire inspired
COLORS = {
    # Primary colors
    "primary": "#8B5CF6",  # Violet
    "primary_dark": "#7C3AED",
    "primary_light": "#A78BFA",
    # Secondary colors
    "secondary": "#06B6D4",  # Cyan
    "secondary_dark": "#0891B2",
    "secondary_light": "#22D3EE",
    # Accent colors
    "accent": "#F59E0B",  # Amber
    "accent_dark": "#D97706",
    "accent_light": "#FBBF24",
    # Semantic colors
    "success": "#10B981",  # Emerald
    "warning": "#F59E0B",  # Amber
    "error": "#EF4444",  # Red
    "info": "#3B82F6",  # Blue
    # Background colors (dark theme)
    "bg_dark": "#0F0F1A",  # Deep dark
    "bg_card": "#1A1A2E",  # Card background
    "bg_elevated": "#252542",  # Elevated elements
    "bg_hover": "#2D2D4A",  # Hover state
    # Text colors
    "text_primary": "#F8FAFC",  # Near white
    "text_secondary": "#94A3B8",  # Muted
    "text_muted": "#64748B",  # Very muted
    # Border colors
    "border": "#3B3B5C",
    "border_accent": "#8B5CF6",
}

# CSS for global styling
GLOBAL_CSS = """
    :root {
        --nicegui-default-padding: 0.75rem;
        --nicegui-default-gap: 0.75rem;
    }

    /* Disable ALL transitions and animations */
    *, *::before, *::after {
        transition: none !important;
        animation: none !important;
        animation-duration: 0s !important;
    }

    body {
        background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%) !important;
        min-height: 100vh;
    }

    /* Glassmorphism card effect */
    .glass-card {
        background: rgba(26, 26, 46, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }

    .glass-card:hover {
        border-color: rgba(139, 92, 246, 0.4) !important;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15) !important;
    }

    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Glow effects */
    .glow-primary {
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
    }

    .glow-subtle {
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    }

    /* Tab styling */
    .q-tab--active {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%) !important;
    }

    .q-tab__indicator {
        background: linear-gradient(90deg, #8B5CF6 0%, #06B6D4 100%) !important;
        height: 3px !important;
    }

    /* Delete badge styling */
    .delete-badge {
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        opacity: 0.7;
    }

    .delete-badge:hover {
        opacity: 1 !important;
        transform: scale(1.1) !important;
    }

    /* Plot container */
    .plot-container {
        background: rgba(26, 26, 46, 0.5) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
        overflow: hidden !important;
        padding: 20px 8px 8px 8px !important;
        position: relative;
        height: 440px !important;
        min-height: 440px !important;
        max-height: 440px !important;
    }

    .plot-container .q-badge {
        position: absolute !important;
        top: 4px !important;
        right: 4px !important;
        z-index: 10;
    }

    .plot-container:hover {
        border-color: rgba(139, 92, 246, 0.4) !important;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15) !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1A1A2E;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #8B5CF6 0%, #06B6D4 100%);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #A78BFA 0%, #22D3EE 100%);
    }

    /* Animation for new elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.4s ease-out;
    }

    /* Button gradients */
    .btn-gradient-danger {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        border: none !important;
    }

    .btn-gradient-primary {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        border: none !important;
    }
"""


def setup_theme():
    """Initialize the theme with custom colors and CSS.

    Call this once at the start of your page.
    """
    # Set Quasar colors
    ui.colors(
        primary=COLORS["primary"],
        secondary=COLORS["secondary"],
        accent=COLORS["accent"],
        dark=COLORS["bg_dark"],
        dark_page=COLORS["bg_dark"],
        positive=COLORS["success"],
        negative=COLORS["error"],
        info=COLORS["info"],
        warning=COLORS["warning"],
    )

    # Add global CSS
    ui.add_css(GLOBAL_CSS)

    # Enable dark mode
    ui.dark_mode(True)


# ============================================================================
# BUTTON FACTORIES
# ============================================================================


def create_btn_delete(on_click: Callable[[], Any]) -> ui.button:
    """Create a styled delete button with icon.

    Args:
        on_click: Callback function when button is clicked.

    Returns:
        Styled delete button.
    """
    btn = ui.button(icon="close", on_click=on_click)
    btn.props("round flat size=sm")
    btn.classes(
        "btn-gradient-danger text-white opacity-70 hover:opacity-100 transition-all"
    )
    btn.style("width: 24px; height: 24px; min-height: 24px;")
    return btn


def create_btn_primary(
    text: str, on_click: Optional[Callable[[], Any]] = None, icon: Optional[str] = None
) -> ui.button:
    """Create a styled primary action button.

    Args:
        text: Button label text.
        on_click: Callback function when button is clicked.
        icon: Optional icon name.

    Returns:
        Styled primary button.
    """
    btn = ui.button(text, on_click=on_click, icon=icon)
    btn.props("rounded unelevated")
    btn.classes("btn-gradient-primary text-white font-medium px-6")
    return btn


def create_btn_secondary(
    text: str, on_click: Optional[Callable[[], Any]] = None, icon: Optional[str] = None
) -> ui.button:
    """Create a styled secondary action button.

    Args:
        text: Button label text.
        on_click: Callback function when button is clicked.
        icon: Optional icon name.

    Returns:
        Styled secondary button.
    """
    btn = ui.button(text, on_click=on_click, icon=icon)
    btn.props("rounded outline")
    btn.classes("text-white border-violet-500 hover:bg-violet-500/20 transition-all")
    return btn


def create_btn_ghost(
    text: str, on_click: Optional[Callable[[], Any]] = None, icon: Optional[str] = None
) -> ui.button:
    """Create a styled ghost/flat button.

    Args:
        text: Button label text.
        on_click: Callback function when button is clicked.
        icon: Optional icon name.

    Returns:
        Styled ghost button.
    """
    btn = ui.button(text, on_click=on_click, icon=icon)
    btn.props("flat rounded")
    btn.classes("text-slate-300 hover:text-white hover:bg-white/10 transition-all")
    return btn


def create_btn_danger(
    text: str, on_click: Optional[Callable[[], Any]] = None, icon: Optional[str] = None
) -> ui.button:
    """Create a styled danger/destructive button.

    Args:
        text: Button label text.
        on_click: Callback function when button is clicked.
        icon: Optional icon name.

    Returns:
        Styled danger button.
    """
    btn = ui.button(text, on_click=on_click, icon=icon)
    btn.props("rounded unelevated")
    btn.classes("btn-gradient-danger text-white font-medium")
    return btn


# ============================================================================
# BADGE FACTORIES
# ============================================================================


def create_delete_badge(on_click: Callable[[Any], Any]) -> ui.badge:
    """Create a floating delete badge (x button).

    Args:
        on_click: Callback function for click event.

    Returns:
        Styled delete badge.
    """
    badge = ui.badge("x")
    badge.props("floating rounded color=red")
    badge.classes("delete-badge cursor-pointer")
    badge.style("font-size: 10px; padding: 2px 6px;")
    badge.on("click", on_click)
    return badge


def create_count_badge(count: int | str, color: str = "primary") -> ui.badge:
    """Create a count/notification badge.

    Args:
        count: Number or text to display.
        color: Badge color (Quasar color name).

    Returns:
        Styled count badge.
    """
    badge = ui.badge(str(count))
    badge.props(f"rounded color={color}")
    badge.classes("text-xs font-bold")
    return badge


# ============================================================================
# CARD & CONTAINER FACTORIES
# ============================================================================


def create_glass_card() -> ui.card:
    """Create a glassmorphism styled card container.

    Returns:
        Styled glass card (use as context manager).
    """
    card = ui.card()
    card.classes("glass-card animate-in")
    return card


def create_elevated_card() -> ui.card:
    """Create an elevated card with subtle shadow.

    Returns:
        Styled elevated card (use as context manager).
    """
    card = ui.card()
    card.classes("glow-subtle rounded-xl")
    card.style(
        f"background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']};"
    )
    return card


def create_plot_container() -> ui.element:
    """Create a container for plot display.

    Returns:
        Styled div container for plots.
    """
    container = ui.element("div")
    container.classes("plot-container p-2 relative")
    return container


def create_section(title: Optional[str] = None) -> ui.element:
    """Create a styled section with optional title.

    Args:
        title: Optional section title.

    Returns:
        Section element (use as context manager).
    """
    section = ui.element("section")
    section.classes("mb-6")
    if title:
        with section:
            create_heading(title, level=2)
    return section


# ============================================================================
# TEXT & LABEL FACTORIES
# ============================================================================


def create_heading(text: str, level: int = 1, gradient: bool = True) -> ui.label:
    """Create a styled heading.

    Args:
        text: Heading text.
        level: Heading level (1-4).
        gradient: Whether to apply gradient text effect.

    Returns:
        Styled label as heading.
    """
    sizes = {
        1: "text-4xl font-bold",
        2: "text-2xl font-semibold",
        3: "text-xl font-medium",
        4: "text-lg font-medium",
    }

    label = ui.label(text)
    label.classes(sizes.get(level, sizes[1]))
    if gradient:
        label.classes("gradient-text")
    else:
        label.style(f"color: {COLORS['text_primary']};")
    return label


def create_label(text: str, muted: bool = False) -> ui.label:
    """Create a styled text label.

    Args:
        text: Label text.
        muted: Whether to use muted/secondary styling.

    Returns:
        Styled label.
    """
    label = ui.label(text)
    if muted:
        label.classes("text-slate-400")
    else:
        label.style(f"color: {COLORS['text_primary']};")
    return label


def create_empty_state(message: str, icon: str = "auto_awesome") -> ui.element:
    """Create a styled empty state message.

    Args:
        message: Message to display.
        icon: Icon name to show.

    Returns:
        Container with empty state styling.
    """
    with ui.column().classes(
        "items-center justify-center py-12 opacity-60"
    ) as container:
        ui.icon(icon, size="xl").classes("text-violet-400 mb-4")
        ui.label(message).classes("text-slate-400 text-lg text-center")
    return container


# ============================================================================
# TAB FACTORIES
# ============================================================================


def create_tabs() -> ui.tabs:
    """Create styled tabs container.

    Returns:
        Styled tabs component.
    """
    tabs = ui.tabs()
    tabs.classes("w-full")
    tabs.props("dense indicator-color=transparent active-color=white")
    tabs.style("""
        background: rgba(26, 26, 46, 0.5);
        border-radius: 12px;
        padding: 4px;
    """)
    return tabs


def create_tab(name: str, icon: Optional[str] = None) -> ui.tab:
    """Create a styled tab.

    Args:
        name: Tab name/label.
        icon: Optional icon name.

    Returns:
        Styled tab component.
    """
    if icon:
        tab = ui.tab(name, icon=icon)
    else:
        tab = ui.tab(name)
    tab.classes("rounded-lg transition-all")
    tab.style("color: #94A3B8;")
    return tab


def create_tab_with_delete(name: str, on_delete: Callable[[Any], Any]) -> ui.tab:
    """Create a tab with a delete badge.

    Args:
        name: Tab name/label.
        on_delete: Callback for delete action.

    Returns:
        Tab with delete badge.
    """
    with ui.tab(name).classes("rounded-lg transition-all") as tab:
        tab.style("color: #94A3B8;")
        create_delete_badge(on_delete)
    return tab


def create_tab_panels(tabs: ui.tabs, value=None) -> ui.tab_panels:
    """Create styled tab panels container.

    Args:
        tabs: Associated tabs component.
        value: Initial selected tab.

    Returns:
        Styled tab panels.
    """
    panels = ui.tab_panels(tabs, value=value)
    panels.classes("w-full")
    panels.style("background: transparent;")
    return panels


def create_tab_panel(name: str) -> ui.tab_panel:
    """Create a styled tab panel.

    Args:
        name: Panel name (must match tab name).

    Returns:
        Styled tab panel.
    """
    panel = ui.tab_panel(name)
    panel.classes("p-4")
    return panel


# ============================================================================
# GRID FACTORIES
# ============================================================================


def create_plot_grid(columns: int = 3) -> ui.grid:
    """Create a responsive grid for plots.

    Args:
        columns: Number of columns.

    Returns:
        Styled grid component.
    """
    grid = ui.grid(columns=columns)
    grid.classes("w-full gap-4 p-4")
    return grid


def create_flex_row(gap: str = "4") -> ui.row:
    """Create a styled flex row.

    Args:
        gap: Tailwind gap value.

    Returns:
        Styled row component.
    """
    row = ui.row()
    row.classes(f"items-center gap-{gap}")
    return row


# ============================================================================
# DIALOG FACTORIES
# ============================================================================


def create_confirm_dialog(
    title: str,
    message: str,
    on_confirm: Callable[[], Any],
    confirm_text: str = "Delete",
    cancel_text: str = "Cancel",
) -> ui.dialog:
    """Create a styled confirmation dialog.

    Args:
        title: Dialog title.
        message: Confirmation message.
        on_confirm: Callback on confirm.
        confirm_text: Confirm button text.
        cancel_text: Cancel button text.

    Returns:
        Dialog component (call .open() to show).
    """
    with ui.dialog() as dialog, create_glass_card():
        ui.label(title).classes("text-xl font-bold text-white mb-2")
        ui.label(message).classes("text-slate-300 mb-6")

        with ui.row().classes("justify-end gap-3"):
            create_btn_ghost(cancel_text, on_click=dialog.close)
            create_btn_danger(
                confirm_text, on_click=lambda: (on_confirm(), dialog.close())
            )

    return dialog


# ============================================================================
# PLOT DISPLAY
# ============================================================================


def create_plotly_chart(fig_data: dict) -> ui.plotly:
    """Create a styled Plotly chart.

    Applies dark theme styling to the chart.

    Args:
        fig_data: Plotly figure data dict.

    Returns:
        Styled plotly component.
    """
    # Ensure dark theme layout
    if "layout" not in fig_data:
        fig_data["layout"] = {}

    layout = fig_data["layout"]
    layout.setdefault("paper_bgcolor", "rgba(0,0,0,0)")
    layout.setdefault("plot_bgcolor", "rgba(26, 26, 46, 0.3)")
    layout.setdefault("font", {"color": "#94A3B8"})
    layout.setdefault("height", 400)  # Fixed height to prevent resize

    # Disable Plotly animations
    layout.setdefault("transition", {"duration": 0})

    # Style axes
    for axis in ["xaxis", "yaxis"]:
        if axis not in layout:
            layout[axis] = {}
        layout[axis].setdefault("gridcolor", "rgba(139, 92, 246, 0.1)")
        layout[axis].setdefault("linecolor", "rgba(139, 92, 246, 0.3)")
        layout[axis].setdefault("tickcolor", "#64748B")

    # Style legend
    layout.setdefault(
        "legend",
        {
            "bgcolor": "rgba(26, 26, 46, 0.8)",
            "bordercolor": "rgba(139, 92, 246, 0.2)",
            "font": {"color": "#94A3B8"},
        },
    )

    chart = ui.plotly(fig_data)
    chart.classes("w-full")
    chart.style("height: 400px; min-height: 400px; max-height: 400px;")
    return chart


# ============================================================================
# HEADER / NAVIGATION
# ============================================================================


def create_header(
    title: str = "GrimoirePlot", subtitle: Optional[str] = None
) -> ui.element:
    """Create a styled page header.

    Args:
        title: Main title text.
        subtitle: Optional subtitle.

    Returns:
        Header container element.
    """
    with ui.element("header").classes("mb-8 text-center py-6") as header:
        # Logo/icon
        ui.icon("auto_stories", size="xl").classes("text-violet-400 mb-2")

        # Title with gradient
        create_heading(title, level=1, gradient=True)

        if subtitle:
            ui.label(subtitle).classes("text-slate-400 mt-2")

    return header


def create_footer() -> ui.element:
    """Create a styled page footer.

    Returns:
        Footer container element.
    """
    with ui.element("footer").classes("mt-auto py-4 text-center") as footer:
        ui.label("GrimoirePlot").classes("text-slate-500 text-sm")
    return footer


# ============================================================================
# LAYOUT HELPERS
# ============================================================================


def create_page_container() -> ui.element:
    """Create the main page container with proper styling.

    Returns:
        Container element (use as context manager).
    """
    container = ui.element("div")
    container.classes(
        "container mx-auto px-4 py-6 max-w-7xl min-h-screen flex flex-col"
    )
    return container


def create_divider() -> ui.element:
    """Create a styled horizontal divider.

    Returns:
        Divider element.
    """
    div = ui.element("hr")
    div.classes("border-0 h-px my-6")
    div.style(
        "background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);"
    )
    return div
