"""
Simple dashboard - just show the data
"""
import json
from pathlib import Path

import dash
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "#0a0e27", "padding": "20px", "minHeight": "100vh"},
    children=[
        html.H1(
            "🥄 AgentSpoons - Volatility Oracle",
            style={"color": "#00d4ff", "textAlign": "center"},
        ),
        html.Div(
            id="metrics",
            style={
                "textAlign": "center",
                "fontSize": "24px",
                "color": "white",
                "margin": "20px",
            },
        ),
        dcc.Graph(id="volatility-chart"),
        dcc.Graph(id="spread-chart"),
        dcc.Interval(id="interval", interval=2000),
    ],
)


@app.callback(
    [Output("metrics", "children"), Output("volatility-chart", "figure"), Output("spread-chart", "figure")],
    [Input("interval", "n_intervals")],
)
def update(n):
    try:
        with open("data/results.json", "r") as f:
            data = json.load(f)
    except Exception:
        data = []

    if not data:
        return "No data yet...", {}, {}

    neo_data = [d for d in data if d.get("pair") == "NEO/USDT"]
    if not neo_data:
        return "Waiting for data...", {}, {}

    latest = neo_data[-1]
    metrics = html.Div(
        [
            html.Div(
                [
                    html.Div("NEO Price", style={"opacity": "0.7"}),
                    html.Div(
                        f"${latest['price']:.2f}",
                        style={"fontSize": "36px", "color": "#00d4ff"},
                    ),
                ],
                style={"display": "inline-block", "margin": "20px"},
            ),
            html.Div(
                [
                    html.Div("Realized Vol", style={"opacity": "0.7"}),
                    html.Div(
                        f"{latest['realized_vol']:.1%}",
                        style={"fontSize": "36px", "color": "#51cf66"},
                    ),
                ],
                style={"display": "inline-block", "margin": "20px"},
            ),
            html.Div(
                [
                    html.Div("Implied Vol", style={"opacity": "0.7"}),
                    html.Div(
                        f"{latest['implied_vol']:.1%}",
                        style={"fontSize": "36px", "color": "#ff6b6b"},
                    ),
                ],
                style={"display": "inline-block", "margin": "20px"},
            ),
        ]
    )

    timestamps = [d.get("timestamp", "")[-8:] for d in neo_data[-20:]]

    vol_fig = go.Figure()
    vol_fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=[d.get("realized_vol", 0) * 100 for d in neo_data[-20:]],
            name="Realized Vol",
            line=dict(color="#51cf66", width=3),
        )
    )
    vol_fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=[d.get("implied_vol", 0) * 100 for d in neo_data[-20:]],
            name="Implied Vol",
            line=dict(color="#ff6b6b", width=3),
        )
    )
    vol_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1a1f3a",
        plot_bgcolor="#1a1f3a",
        title="Volatility Comparison",
        yaxis_title="Volatility %",
    )

    spread_fig = go.Figure()
    spread_fig.add_trace(
        go.Bar(
            x=timestamps,
            y=[d.get("spread", 0) * 100 for d in neo_data[-20:]],
            marker_color="#00d4ff",
        )
    )
    spread_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1a1f3a",
        plot_bgcolor="#1a1f3a",
        title="IV - RV Spread (Arbitrage Opportunity)",
        yaxis_title="Spread %",
    )

    return metrics, vol_fig, spread_fig


if __name__ == "__main__":
    print("🚀 Dashboard running at http://localhost:8050")
    app.run_server(debug=False, host="0.0.0.0", port=8050)
