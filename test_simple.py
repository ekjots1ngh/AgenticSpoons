import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Test - If you see this, it works!", style={'color': 'white'}),
    html.P("Dashboard is running successfully")
], style={'backgroundColor': '#0f172a', 'padding': '50px', 'minHeight': '100vh'})

if __name__ == '__main__':
    print("="*70)
    print("🧪 TEST SERVER")
    print("="*70)
    print("🌐 URL: http://127.0.0.1:8888")
    print("="*70)
    
    try:
        app.run_server(
            debug=True,
            port=8888,
            host='127.0.0.1'
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTry these commands:")
        print("1. pip install --upgrade dash dash-bootstrap-components")
        print("2. python test_simple.py")
