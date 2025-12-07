# Dark/Light Theme Toggle Implementation Guide

## Overview
The AgentSpoons dashboard now supports dynamic theme switching between Dark and Light modes with persistent theme selection.

## What Was Implemented

### 1. **Centralized Theme Module** ([src/dashboard/themes.py](src/dashboard/themes.py))
- `DARK_COLORS` - Dark theme color palette (default)
- `LIGHT_COLORS` - Light theme color palette
- `get_colors(theme)` - Returns color scheme for specified theme
- `get_plotly_template(theme)` - Returns appropriate Plotly template
- `get_chart_colors(theme)` - Returns optimized chart colors

### 2. **Updated Championship Dashboard** ([src/championship_dashboard.py](src/championship_dashboard.py))
- Added Font Awesome icons for theme toggle button
- Theme toggle button in header (moon/sun icon)
- `dcc.Store` component for persistent theme storage (localStorage)
- Theme toggle callback to switch between dark/light modes
- Updated main dashboard callback to use dynamic colors
- All charts now respond to theme changes

## How It Works

### Theme Toggle Flow
1. User clicks "Theme" button in header
2. `toggle_theme` callback switches between 'dark' and 'light'
3. Theme preference saved to browser localStorage
4. Icon changes: 🌙 (moon) for dark mode, ☀️ (sun) for light mode
5. `update_dashboard` callback receives theme change
6. All components re-render with new color scheme

### Color Adaptation
- **Background colors** - Switch from dark navy to light gray
- **Card colors** - Switch from dark panels to white
- **Text colors** - Switch from white to dark gray
- **Chart templates** - Switch from `plotly_dark` to `plotly_white`
- **Chart colors** - Optimized for contrast in each theme

## Usage

### Running the Dashboard
```bash
cd agentspoons
python src/championship_dashboard.py
```

Then visit: `http://localhost:8050`

### Using the Theme Toggle
1. Look for the "Theme" button in the top-right header (next to LIVE badge)
2. Click to toggle between Dark and Light modes
3. Theme preference persists across browser sessions

## Applying Themes to Other Dashboards

To add theme support to other dashboards in your codebase:

### Step 1: Import Theme Module
```python
from dashboard.themes import get_colors, get_plotly_template, get_chart_colors
```

### Step 2: Add Theme Store
```python
# In your layout
dcc.Store(id='theme-store', storage_type='local', data='dark')
```

### Step 3: Add Theme Toggle Button
```python
dbc.Button(
    id='theme-toggle',
    children=[
        html.I(className='fas fa-moon', id='theme-icon', style={'marginRight': '8px'}),
        html.Span('Theme')
    ],
    color='secondary',
    outline=True,
    size='sm'
)
```

### Step 4: Add Toggle Callback
```python
@app.callback(
    [Output('theme-store', 'data'),
     Output('theme-icon', 'className')],
    [Input('theme-toggle', 'n_clicks')],
    [State('theme-store', 'data')]
)
def toggle_theme(n_clicks, current_theme):
    if n_clicks is None:
        icon = 'fas fa-sun' if current_theme == 'light' else 'fas fa-moon'
        return current_theme or 'dark', icon

    new_theme = 'light' if current_theme == 'dark' else 'dark'
    icon = 'fas fa-sun' if new_theme == 'light' else 'fas fa-moon'
    return new_theme, icon
```

### Step 5: Update Main Callback
```python
@app.callback(
    [...outputs...],
    [Input('interval', 'n_intervals'),
     Input('theme-store', 'data')]  # Add theme input
)
def update_dashboard(n, theme):
    # Get theme colors
    COLORS = get_colors(theme or 'dark')
    chart_colors = get_chart_colors(theme or 'dark')
    plotly_template = get_plotly_template(theme or 'dark')

    # Use COLORS and chart_colors in your components
    # Use plotly_template in chart layouts
```

## Dashboards to Update

Apply the same pattern to these dashboards:
- [src/dashboard/analytics_dashboard.py](src/dashboard/analytics_dashboard.py)
- [src/dashboard/bloomberg_layout.py](src/dashboard/bloomberg_layout.py)
- [src/dashboard/advanced_app.py](src/dashboard/advanced_app.py)
- [src/visualization/enhanced_dashboard.py](src/visualization/enhanced_dashboard.py)
- [src/visualization/greeks_dashboard.py](src/visualization/greeks_dashboard.py)

## Theme Customization

### Modifying Colors
Edit [src/dashboard/themes.py](src/dashboard/themes.py) to customize color schemes:

```python
LIGHT_COLORS = {
    'background': '#your-color',
    'card': '#your-color',
    'primary': '#your-color',
    # ... etc
}
```

### Adding New Themes
You can extend the system to support more themes:

1. Add new color dictionary to `themes.py`
2. Update `get_colors()` function
3. Add theme selection dropdown instead of toggle button

## Technical Details

### Browser Storage
- Theme preference stored in `localStorage`
- Key: `theme-store`
- Values: `'dark'` or `'light'`
- Persists across browser sessions

### Performance
- Theme changes trigger single callback re-render
- No page reload required
- Smooth transitions via Plotly's `transition_duration`

### Accessibility
- High contrast maintained in both themes
- Clear visual indicators for theme state
- Icon changes provide visual feedback

## Troubleshooting

### Theme not persisting
- Check browser localStorage is enabled
- Clear browser cache and try again

### Charts not updating colors
- Ensure all charts use `plotly_template` variable
- Check that `chart_colors` is used instead of hardcoded colors

### Button not appearing
- Verify Font Awesome CDN is loaded
- Check browser console for errors

## Next Steps

### Recommended Enhancements
1. Add theme preview thumbnails
2. Create custom color picker for user-defined themes
3. Add theme presets (e.g., "Bloomberg", "Mint", "Sunset")
4. Sync theme across multiple tabs
5. Add transition animations for smoother theme changes

### Integration with Other Components
- Apply theme to email reports
- Export charts with theme-appropriate colors
- Match Neo blockchain integration UI to theme

## Support

For issues or questions about theme implementation:
1. Check this guide first
2. Review [src/dashboard/themes.py](src/dashboard/themes.py) for available functions
3. Examine [src/championship_dashboard.py](src/championship_dashboard.py) for reference implementation

## License
Part of the AgentSpoons project - Neo Blockchain Hackathon Entry
