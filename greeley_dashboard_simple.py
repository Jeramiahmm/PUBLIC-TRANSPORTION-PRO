"""
GREELEY SMART TRANSIT DASHBOARD - STANDALONE VERSION
Complete dashboard in a single file - just run this!

SETUP:
1. Save this file as: greeley_dashboard.py
2. Install packages: pip install pandas plotly dash dash-bootstrap-components openpyxl
3. Put "New KPI Tracker.xlsx" in the same folder as this file
4. Run: python greeley_dashboard.py
5. Open browser: http://localhost:8050

Author: COOLER BLAST Initiative - UNC
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
import os

# ============================================================================
# DATA LOADING
# ============================================================================

def load_greeley_data(filepath='New KPI Tracker.xlsx'):
    """Load and clean Greeley transit data"""
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Cannot find data file: {filepath}\n"
                              f"   Please put 'New KPI Tracker.xlsx' in the same folder as this script!")
    
    print(f"📊 Loading data from: {filepath}")
    xl = pd.ExcelFile(filepath)
    df = pd.read_excel(xl, sheet_name='Ridership', skiprows=1)
    
    # Fixed Route (main service)
    fixed_route = df.iloc[:, 0:2].copy()
    fixed_route.columns = ['Date', 'Ridership']
    fixed_route = fixed_route.dropna(subset=['Ridership'])
    fixed_route['Date'] = pd.to_datetime(fixed_route['Date'], errors='coerce')
    fixed_route = fixed_route[fixed_route['Date'].notna()].reset_index(drop=True)
    fixed_route['Year'] = fixed_route['Date'].dt.year
    fixed_route['Month'] = fixed_route['Date'].dt.month
    fixed_route['Quarter'] = fixed_route['Date'].dt.quarter
    fixed_route['Month_Name'] = fixed_route['Date'].dt.month_name()
    fixed_route['MA_12'] = fixed_route['Ridership'].rolling(window=12, center=True).mean()
    
    # Paratransit
    paratransit = df.iloc[:, 18:20].copy()
    paratransit.columns = ['Date', 'Ridership']
    paratransit = paratransit.dropna(subset=['Ridership'])
    paratransit['Date'] = pd.to_datetime(paratransit['Date'], errors='coerce')
    paratransit = paratransit[paratransit['Date'].notna()].reset_index(drop=True)
    paratransit['Year'] = paratransit['Date'].dt.year
    
    # UNC Student
    unc = df.iloc[:, 39:41].copy()
    unc.columns = ['Date', 'Ridership']
    unc = unc.dropna(subset=['Ridership'])
    unc['Date'] = pd.to_datetime(unc['Date'], errors='coerce')
    unc = unc[unc['Date'].notna()].reset_index(drop=True)
    unc['Year'] = unc['Date'].dt.year
    
    print(f"✅ Loaded {len(fixed_route)} months of data ({fixed_route['Date'].min().year}-{fixed_route['Date'].max().year})")
    
    return {'fixed_route': fixed_route, 'paratransit': paratransit, 'unc': unc}

# ============================================================================
# VISUALIZATIONS
# ============================================================================

def create_timeline_chart(df):
    """Create ridership timeline with COVID annotation"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Ridership'],
        mode='lines', name='Monthly Ridership',
        line=dict(color='#2E86AB', width=2),
        hovertemplate='<b>%{x|%B %Y}</b><br>Ridership: %{y:,.0f}<extra></extra>'
    ))
    
    if 'MA_12' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['MA_12'],
            mode='lines', name='12-Month Avg',
            line=dict(color='#A23B72', width=2, dash='dash'),
            hovertemplate='<b>%{x|%B %Y}</b><br>12-Mo Avg: %{y:,.0f}<extra></extra>'
        ))
    
    fig.add_vrect(x0="2020-03-01", x1="2021-12-31",
                  fillcolor="red", opacity=0.1, layer="below", line_width=0,
                  annotation_text="COVID-19", annotation_position="top left")
    
    fig.update_layout(
        title="Greeley Transit Ridership Timeline (2014-2025)",
        xaxis_title="Date", yaxis_title="Monthly Ridership",
        hovermode='x unified', template='plotly_white', height=500
    )
    return fig

def create_yearly_bars(df):
    """Create annual comparison bars"""
    yearly = df.groupby('Year')['Ridership'].sum().reset_index()
    colors = ['#E63946' if 2020 <= year <= 2021 else '#2E86AB' for year in yearly['Year']]
    
    fig = go.Figure(data=[go.Bar(
        x=yearly['Year'], y=yearly['Ridership'],
        marker_color=colors, text=yearly['Ridership'],
        texttemplate='%{text:,.0f}', textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Annual Ridership Comparison",
        xaxis_title="Year", yaxis_title="Total Ridership",
        template='plotly_white', height=500, showlegend=False
    )
    return fig

def create_heatmap(df):
    """Create seasonal heatmap"""
    pivot = df.pivot_table(values='Ridership', index='Year', columns='Month', aggfunc='sum')
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=month_names, y=pivot.index,
        colorscale='YlOrRd',
        hovertemplate='<b>%{y} - %{x}</b><br>Ridership: %{z:,.0f}<extra></extra>',
        colorbar=dict(title="Ridership")
    ))
    
    fig.update_layout(
        title="Ridership Heatmap by Month and Year",
        xaxis_title="Month", yaxis_title="Year",
        template='plotly_white', height=600
    )
    return fig

def create_monthly_avg(df):
    """Create monthly averages bar chart"""
    monthly_avg = df.groupby('Month')['Ridership'].mean().reset_index()
    monthly_avg['Month_Name'] = pd.to_datetime(monthly_avg['Month'], format='%m').dt.month_name()
    colors = ['#F77F00' if m in [6,7,8] else '#2E86AB' for m in monthly_avg['Month']]
    
    fig = go.Figure(data=[go.Bar(
        x=monthly_avg['Month_Name'], y=monthly_avg['Ridership'],
        marker_color=colors, text=monthly_avg['Ridership'],
        texttemplate='%{text:,.0f}', textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg: %{y:,.0f}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Average Ridership by Month (All Years)",
        xaxis_title="Month", yaxis_title="Average Ridership",
        template='plotly_white', height=500, showlegend=False
    )
    return fig

def create_service_comparison(data):
    """Compare different services"""
    fig = go.Figure()
    colors = {'fixed_route': '#2E86AB', 'paratransit': '#A23B72', 'unc': '#F77F00'}
    
    for service_name, df in data.items():
        if len(df) > 0:
            yearly = df.groupby('Year')['Ridership'].sum().reset_index()
            fig.add_trace(go.Scatter(
                x=yearly['Year'], y=yearly['Ridership'],
                mode='lines+markers',
                name=service_name.replace('_', ' ').title(),
                line=dict(color=colors.get(service_name, '#333'), width=2),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        title="Service Type Comparison",
        xaxis_title="Year", yaxis_title="Annual Ridership",
        hovermode='x unified', template='plotly_white', height=500
    )
    return fig

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n" + "="*70)
print("🚌 GREELEY SMART TRANSIT DASHBOARD")
print("="*70)

try:
    data = load_greeley_data()
    fixed_route = data['fixed_route']
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 QUICK FIX:")
    print("   1. Make sure 'New KPI Tracker.xlsx' is in the same folder")
    print("   2. Or edit line 42 to point to your file location")
    exit(1)

# Calculate metrics
latest_year = fixed_route['Year'].max()
prev_year = latest_year - 1
latest_month = fixed_route[fixed_route['Year'] == latest_year].tail(1)
latest_ridership = latest_month['Ridership'].values[0] if len(latest_month) > 0 else 0
annual_total = fixed_route[fixed_route['Year'] == latest_year]['Ridership'].sum()

# YoY calculation
ytd_current = fixed_route[fixed_route['Year'] == latest_year]['Ridership'].sum()
max_month_current = fixed_route[fixed_route['Year'] == latest_year]['Month'].max()
ytd_prev = fixed_route[(fixed_route['Year'] == prev_year) & 
                       (fixed_route['Month'] <= max_month_current)]['Ridership'].sum()
yoy_change = ((ytd_current - ytd_prev) / ytd_prev * 100) if ytd_prev > 0 else 0

pre_covid = fixed_route[fixed_route['Year'] == 2019]['Ridership'].sum()
recovery_pct = (annual_total / pre_covid * 100) if pre_covid > 0 else 0

# ============================================================================
# DASHBOARD APP
# ============================================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Greeley Transit Dashboard"

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🚌 Greeley Smart Transit Dashboard", className="text-center mb-2"),
            html.P("Interactive Analysis of Public Transit Data (2014-2025)", 
                  className="text-center text-muted mb-4"),
            html.P("COOLER BLAST Initiative - University of Northern Colorado", 
                  className="text-center text-muted small")
        ])
    ]),
    
    html.Hr(),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Latest Month", className="text-muted"),
                    html.H3(f"{latest_ridership:,.0f}", className="text-primary"),
                    html.P(f"{latest_month['Date'].dt.strftime('%B %Y').values[0] if len(latest_month) > 0 else 'N/A'}", 
                          className="small mb-0")
                ])
            ])
        ], md=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6(f"{latest_year} YTD Total", className="text-muted"),
                    html.H3(f"{annual_total:,.0f}", className="text-primary"),
                    html.P(f"{yoy_change:+.1f}% vs {prev_year}", 
                          className="small mb-0",
                          style={"color": "green" if yoy_change > 0 else "red"})
                ])
            ])
        ], md=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("COVID Recovery", className="text-muted"),
                    html.H3(f"{recovery_pct:.0f}%", className="text-primary"),
                    html.P("of 2019 levels", className="small mb-0")
                ])
            ])
        ], md=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Data Range", className="text-muted"),
                    html.H3(f"{len(fixed_route)}", className="text-primary"),
                    html.P("months", className="small mb-0")
                ])
            ])
        ], md=3),
    ], className="mb-4"),
    
    # Tabs
    dbc.Tabs([
        dbc.Tab(label="📊 Overview", tab_id="overview"),
        dbc.Tab(label="📈 Timeline", tab_id="timeline"),
        dbc.Tab(label="🗓️ Seasonal", tab_id="seasonal"),
        dbc.Tab(label="🚌 Services", tab_id="services"),
    ], id="tabs", active_tab="overview", className="mb-4"),
    
    html.Div(id="tab-content"),
    
    # Footer
    html.Hr(className="mt-5"),
    html.Footer([
        html.P([
            "Data: Greeley Transit | Created by COOLER BLAST Initiative, UNC | ",
            f"Updated: {pd.Timestamp.now().strftime('%B %d, %Y')}"
        ], className="text-center text-muted small")
    ])
    
], fluid=True, className="py-4")

@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab(active_tab):
    if active_tab == "overview":
        return dbc.Container([
            dbc.Row([dbc.Col([
                html.H4("The Story: COVID Recovery & 2025 Decline", className="mb-3"),
                html.P([
                    f"Greeley Transit recovered to {recovery_pct:.0f}% of pre-pandemic levels by 2024. ",
                    html.Strong(f"However, 2025 shows a {abs(yoy_change):.0f}% decline "),
                    "that needs investigation."
                ], className="lead"),
            ])]),
            dbc.Row([dbc.Col([dcc.Graph(figure=create_timeline_chart(fixed_route))])]),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=create_yearly_bars(fixed_route))], md=6),
                dbc.Col([dcc.Graph(figure=create_monthly_avg(fixed_route))], md=6),
            ]),
        ])
    
    elif active_tab == "timeline":
        return dbc.Container([
            dbc.Row([dbc.Col([
                html.H4("Detailed Timeline Analysis", className="mb-3"),
                dcc.Graph(figure=create_timeline_chart(fixed_route))
            ])]),
            dbc.Row([
                dbc.Col([
                    html.H5("Key Patterns:", className="mt-4"),
                    html.Ul([
                        html.Li("2014-2019: Steady growth (+54%)"),
                        html.Li("2020: COVID crash (-56%)"),
                        html.Li("2021-2024: Recovery phase"),
                        html.Li(f"2025: Decline ({yoy_change:.1f}% YTD)"),
                    ])
                ])
            ])
        ])
    
    elif active_tab == "seasonal":
        return dbc.Container([
            dbc.Row([dbc.Col([
                html.H4("Seasonal Patterns", className="mb-3"),
                dcc.Graph(figure=create_heatmap(fixed_route))
            ])]),
            dbc.Row([dbc.Col([
                dcc.Graph(figure=create_monthly_avg(fixed_route))
            ])], className="mt-4"),
        ])
    
    elif active_tab == "services":
        return dbc.Container([
            dbc.Row([dbc.Col([
                html.H4("Service Comparison", className="mb-3"),
                dcc.Graph(figure=create_service_comparison(data))
            ])]),
            dbc.Row([dbc.Col([
                html.H5("Service Types:", className="mt-4"),
                html.Ul([
                    html.Li([html.Strong("Fixed Route: "), "Primary bus service (9 routes)"]),
                    html.Li([html.Strong("Paratransit: "), "ADA on-demand service"]),
                    html.Li([html.Strong("UNC: "), "University partnership service"]),
                ])
            ])])
        ])
    
    return html.Div("Select a tab")

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    print(f"\n✅ Dashboard ready!")
    print(f"📊 Data: {len(fixed_route)} months from {fixed_route['Date'].min().year}-{fixed_route['Date'].max().year}")
    print(f"\n🌐 Opening dashboard at: http://localhost:8050")
    print("   Press CTRL+C to stop\n")
    print("="*70 + "\n")
    
    app.run_server(debug=True, port=8050)
