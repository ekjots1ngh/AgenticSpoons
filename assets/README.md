# Assets Directory

This directory is for static assets used by Dash dashboards.

## Purpose
Dash automatically serves files from the `assets/` directory.

## Potential Files
- **CSS files** - Custom stylesheets
- **JavaScript files** - Client-side scripts
- **Images** - Logos, icons, backgrounds
- **Fonts** - Custom typography

## Theme System
The theme toggle system uses:
- Font Awesome icons (loaded via CDN)
- Dynamic color management (via Python callbacks)
- No custom CSS required currently

## Future Enhancements
You could add:
- `custom.css` - For smooth color transitions
- `theme-animations.css` - For theme switch animations
- `logo.png` - AgentSpoons logo
- `favicon.ico` - Browser tab icon

## Note
This directory was created to support the Dash application structure.
Currently, theme colors are managed entirely through Python callbacks.
