"""
Theme Configuration for AgentSpoons Dashboards
Centralized theme management for dark/light mode toggle
"""

# Dark Theme Colors (Default)
DARK_COLORS = {
    'background': '#0a0e27',
    'card': '#1a1f3a',
    'primary': '#00d4ff',
    'success': '#51cf66',
    'warning': '#ffd43b',
    'danger': '#ff6b6b',
    'text': '#ffffff',
    'muted': '#8b92a8',
    'border': '#2a2f4a'
}

# Light Theme Colors
LIGHT_COLORS = {
    'background': '#f5f7fa',
    'card': '#ffffff',
    'primary': '#0088cc',
    'success': '#2d8659',
    'warning': '#e09f3e',
    'danger': '#d62828',
    'text': '#1a1a1a',
    'muted': '#6c757d',
    'border': '#dee2e6'
}

# Plotly template names
PLOTLY_TEMPLATES = {
    'dark': 'plotly_dark',
    'light': 'plotly_white'
}

# Bootstrap theme URLs
BOOTSTRAP_THEMES = {
    'dark': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cyborg/bootstrap.min.css',
    'light': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/flatly/bootstrap.min.css'
}

def get_colors(theme='dark'):
    """
    Get color scheme for specified theme

    Args:
        theme: 'dark' or 'light'

    Returns:
        Dictionary of color values
    """
    return LIGHT_COLORS if theme == 'light' else DARK_COLORS

def get_plotly_template(theme='dark'):
    """
    Get Plotly template name for specified theme

    Args:
        theme: 'dark' or 'light'

    Returns:
        Plotly template string
    """
    return PLOTLY_TEMPLATES.get(theme, 'plotly_dark')

def get_chart_colors(theme='dark'):
    """
    Get optimized chart colors for theme

    Args:
        theme: 'dark' or 'light'

    Returns:
        Dictionary of chart-specific colors
    """
    if theme == 'light':
        return {
            'success_line': '#2d8659',
            'success_fill': 'rgba(45, 134, 89, 0.15)',
            'danger_line': '#d62828',
            'danger_fill': 'rgba(214, 40, 40, 0.15)',
            'primary_line': '#0088cc',
            'primary_fill': 'rgba(0, 136, 204, 0.15)',
            'grid': '#e0e0e0',
            'zero_line': '#999999'
        }
    else:
        return {
            'success_line': '#51cf66',
            'success_fill': 'rgba(81, 207, 102, 0.1)',
            'danger_line': '#ff6b6b',
            'danger_fill': 'rgba(255, 107, 107, 0.1)',
            'primary_line': '#00d4ff',
            'primary_fill': 'rgba(0, 212, 255, 0.1)',
            'grid': '#2a2f4a',
            'zero_line': '#8b92a8'
        }
