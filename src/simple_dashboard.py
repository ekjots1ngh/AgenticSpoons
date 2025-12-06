"""
FIXED Simple Dashboard
"""
import json
import os

import dash
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#0a0e27",
        "padding": "20px",
        "minHeight": "100vh",
        "fontFamily": "Arial",
    },
    children=[
        html.H1(
            "🥄 AgentSpoons - Volatility Oracle",
            style={"color": "#00d4ff", "textAlign": "center", "marginBottom": "30px"},
        ),
        html.Div(
            id="status",
            style={"textAlign": "center", "color": "#51cf66", "fontSize": "18px"},
        ),
        html.Div(
            id="metrics",
            style={
                "textAlign": "center",
                "color": "white",
                "margin": "30px 0",
                "display": "flex",
                "justifyContent": "center",
                "gap": "40px",
            },
        ),
        html.Div(
            [
                dcc.Graph(id="volatility-chart", style={"margin": "20px 0"}),
                dcc.Graph(id="spread-chart", style={"margin": "20px 0"}),
            ]
        ),
        dcc.Interval(id="interval", interval=2000),
    ],
)


def load_data():
    """Load data with error handling"""
    try:
        filepath = "data/results.json"
        if not os.path.exists(filepath):
            return None, "⏳ Waiting for data file..."

        with open(filepath, "r") as f:
            data = json.load(f)

        if not data:
            return None, "⏳ Data file empty, waiting..."

        return data, f"✅ Live - {len(data)} data points"

    except json.JSONDecodeError:
        return None, "⚠️ Data file corrupted, regenerating..."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


@app.callback(
    Output("status", "children"),
    Output("metrics", "children"),
    Output("volatility-chart", "figure"),
    Output("spread-chart", "figure"),
    Input("interval", "n_intervals"),
)
def update(n):
    data, status = load_data()

    if data is None:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1a1f3a",
            plot_bgcolor="#1a1f3a",
            title="Waiting for data...",
        )
        return status, [], empty_fig, empty_fig

    neo_data = [d for d in data if d["pair"] == "NEO/USDT"][-50:]

    if not neo_data:
        empty_fig = go.Figure()
        empty_fig.update_layout(template="plotly_dark", paper_bgcolor="#1a1f3a")
        return "⏳ Waiting for NEO data...", [], empty_fig, empty_fig

    latest = neo_data[-1]

    metrics = [
        html.Div(
            [
                html.Div("💰 NEO Price", style={"opacity": "0.7", "fontSize": "14px"}),
                html.Div(
                    f"${latest['price']:.2f}",
                    style={"fontSize": "32px", "color": "#00d4ff", "fontWeight": "bold"},
                ),
            ],
            style={"backgroundColor": "#1a1f3a", "padding": "20px", "borderRadius": "10px"},
        ),
        html.Div(
            [
                html.Div("📊 Realized Vol", style={"opacity": "0.7", "fontSize": "14px"}),
                html.Div(
                    f"{latest['realized_vol']*100:.1f}%",
                    style={"fontSize": "32px", "color": "#51cf66", "fontWeight": "bold"},
                ),
            ],
            style={"backgroundColor": "#1a1f3a", "padding": "20px", "borderRadius": "10px"},
        ),
        html.Div(
            [
                html.Div("🎯 Implied Vol", style={"opacity": "0.7", "fontSize": "14px"}),
                html.Div(
                    f"{latest['implied_vol']*100:.1f}%",
                    style={"fontSize": "32px", "color": "#ff6b6b", "fontWeight": "bold"},
                ),
            ],
            style={"backgroundColor": "#1a1f3a", "padding": "20px", "borderRadius": "10px"},
        ),
        html.Div(
            [
                html.Div("💡 Spread", style={"opacity": "0.7", "fontSize": "14px"}),
                html.Div(
                    f"{latest['spread']*100:.1f}%",
                    style={"fontSize": "32px", "color": "#ffd43b", "fontWeight": "bold"},
                ),
            ],
            style={"backgroundColor": "#1a1f3a", "padding": "20px", "borderRadius": "10px"},
        ),
    ]

    vol_fig = go.Figure()
    vol_fig.add_trace(
        go.Scatter(
            y=[d["realized_vol"] * 100 for d in neo_data],
            mode="lines+markers",
            name="Realized Vol",
            line=dict(color="#51cf66", width=3),
            marker=dict(size=6),
        )
    )
    vol_fig.add_trace(
        go.Scatter(
            y=[d["implied_vol"] * 100 for d in neo_data],
            mode="lines+markers",
            name="Implied Vol",
            line=dict(color="#ff6b6b", width=3),
            marker=dict(size=6),
        )
    )
    vol_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1a1f3a",
        plot_bgcolor="#1a1f3a",
        title="Volatility Comparison (Real-time)",
        yaxis_title="Volatility %",
        xaxis_title="Time",
        hovermode="x unified",
        height=400,
    )

    spread_fig = go.Figure()
    spread_fig.add_trace(
        go.Bar(
            y=[d["spread"] * 100 for d in neo_data],
            marker_color="#00d4ff",
            hovertemplate="Spread: %{y:.2f}%<extra></extra>",
        )
    )
    spread_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1a1f3a",
        plot_bgcolor="#1a1f3a",
        title="IV - RV Spread (Arbitrage Signal)",
        yaxis_title="Spread %",
        xaxis_title="Time",
        height=400,
    )

    return status, metrics, vol_fig, spread_fig


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AgentSpoons Dashboard Starting...")
    print("=" * 60)
    print("📍 Open browser: http://localhost:8050")
    print("⏱️  Updates every 2 seconds")
    print("=" * 60 + "\n")

    app.run(debug=False, host="0.0.0.0", port=8050)
