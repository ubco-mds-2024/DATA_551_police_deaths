import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
import webbrowser
import plotly.express as px

# =================================================
# 1. Load the CSV data
# =================================================
file_path = 'data/clean_data.csv'
data = pd.read_csv(file_path)

# If 'state' might have inconsistent cases or extra spaces, do this:
# data['state'] = data['state'].str.upper().str.strip()

# =================================================
# 2. Disable Altair’s max row limit
# =================================================
alt.data_transformers.disable_max_rows()

# =================================================
# 3. Initialize Dash
# =================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Police Officer Deaths Dashboard"

# =================================================
# 4. State Abbreviation -> FIPS Mapping
# =================================================
state_abbrev_to_fips = {
    'AL': 1, 'AK': 2, 'AZ': 4, 'AR': 5, 'CA': 6, 'CO': 8, 'CT': 9,
    'DE': 10, 'DC': 11, 'FL': 12, 'GA': 13, 'HI': 15, 'ID': 16,
    'IL': 17, 'IN': 18, 'IA': 19, 'KS': 20, 'KY': 21, 'LA': 22,
    'ME': 23, 'MD': 24, 'MA': 25, 'MI': 26, 'MN': 27, 'MS': 28,
    'MO': 29, 'MT': 30, 'NE': 31, 'NV': 32, 'NH': 33, 'NJ': 34,
    'NM': 35, 'NY': 36, 'NC': 37, 'ND': 38, 'OH': 39, 'OK': 40,
    'OR': 41, 'PA': 42, 'RI': 44, 'SC': 45, 'SD': 46, 'TN': 47,
    'TX': 48, 'UT': 49, 'VT': 50, 'VA': 51, 'WA': 53, 'WV': 54,
    'WI': 55, 'WY': 56
}

# =================================================
# 5. Add a fips column for map matching
# =================================================
data['fips'] = data['state'].map(state_abbrev_to_fips)

# =================================================
# 6. Summary statistic function
# =================================================
def compute_summary_stats(filtered_data):
    total_deaths = len(filtered_data)
    year_min = filtered_data['year'].min()
    year_max = filtered_data['year'].max()
    if pd.isna(year_min) or pd.isna(year_max):
        return 0, 0, 0
    
    year_span = year_max - year_min + 1
    avg_per_year = total_deaths / year_span if year_span > 0 else 0

    first_year_count = filtered_data[filtered_data['year'] == year_min].shape[0]
    last_year_count = filtered_data[filtered_data['year'] == year_max].shape[0]
    year_change = ((last_year_count - first_year_count) / first_year_count * 100) if first_year_count > 0 else 0
    
    return total_deaths, avg_per_year, year_change

# =================================================
# 7. Chart-building helper functions
# =================================================
def create_bar_chart(data, x_col, y_col, title):
    """Builds a bar chart."""
    if data.empty:
        return None
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(x_col),
            y=alt.Y(y_col,sort='-x'),
            color=alt.Color(y_col, legend=None),
            tooltip=[x_col, y_col]
        )
        .properties(title=title, width=500, height=400)
    )
    return chart

def create_time_series(data, x_col, y_col, title):
    """Builds a line chart (time series)."""
    if data.empty:
        return None
    chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X(x_col, title='Year'),
            y=alt.Y(y_col, title='Number of Deaths'),
            tooltip=[x_col, y_col]
        )
        .properties(title=title, width=500, height=400)
    )
    return chart


def create_us_heatmap(filtered_data):
    # Count occurrences of each state
    state_counts = filtered_data["state"].value_counts().reset_index()
    state_counts.columns = ["state", "count"]  # rename column
    state_counts["state"] = state_counts["state"].str.strip()
    print(state_counts)
    # Create the choropleth map
    fig = px.choropleth(
        state_counts,
        locations="state",
        locationmode="USA-states",
        color="count",
        color_continuous_scale="reds",
        scope="usa",
        title="Mapping Fallen Officers: U.S. Deaths by State",
    )
    return fig

# =================================================
# 8. Sidebar: user filters
# =================================================
def create_multiselect_dropdown(id, options):
    return html.Div([
        dcc.Checklist(
            id=id,
            options=options,
            value=[opt['value'] for opt in options[1:]],
            inline=False,
            inputStyle={"margin-right": "5px"}
        )
    ], style={"max-height": "200px", "overflow-y": "auto", "border": "1px solid #ccc", "padding": "5px"})

cause_options = [{'label': 'Select All', 'value': 'ALL'}] + [{'label': c, 'value': c} for c in sorted(data['cause_short'].unique())]
state_options = [{'label': 'Select All', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in sorted(data['state'].unique())]

canine_filter = html.Div([
    html.Label("Select Officer Type:", style={"font-weight": "bold", "margin-right": "10px"}),
    dbc.ButtonGroup([
        dbc.Button("Police", id="police-button", color="primary", outline=False, n_clicks=1), 
        dbc.Button("Canine", id="canine-button", color="primary", outline=False, n_clicks=1), 
    ])
], style={"text-align": "right", "margin-bottom": "10px"})

sidebar = html.Div([
    html.Label("Filter by Year"),
    dcc.RangeSlider(
        id='year-filter',
        min=data['year'].min(),
        max=data['year'].max(),
        marks={i: str(i) for i in range(data['year'].min(), data['year'].max()+1, 50)},
        step=1,
        value=[data['year'].min(), data['year'].max()],
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Div(id='year-display', style={"font-weight": "bold", "margin-top": "5px"}),
    html.Br(),
    html.Label("Filter by Cause"),
    create_multiselect_dropdown('cause-filter', cause_options),
    html.Br(),
    html.Label("Filter by State"),
    create_multiselect_dropdown('state-filter', state_options),
])


# =================================================
# 9. Summary stats area
# =================================================
summary_section = html.Div(id='summary-stats')

# =================================================
# 10. Main layout
# =================================================
# Add the button group back in the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Police Officer Deaths Dashboard"), width=9),
        dbc.Col(canine_filter, width=3, style={"text-align": "right"})  # Aligns to top-right
    ], align="center", className="mb-3"),
    
    dbc.Row([
        dbc.Col(sidebar, width=3, style={"border-right": "1px solid #ccc", "padding-right": "15px"}),
        
        dbc.Col([
            # Summary stats in horizontal boxes
            dbc.Row([
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Total Deaths"), html.P(id="total-deaths")])]), width=4),
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Average Deaths per Year"), html.P(id="avg-deaths")])]), width=4),
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Annual Growth Rate"), html.P(id="growth-rate")])]), width=4)
            ], className="mb-3"),
            
            dbc.Row([
                # Left side (Time Series on top, Bar Charts below it)
                dbc.Col([
                    html.Iframe(id='time-series', style={'width': '100%', 'height': '400px'}),
                    dbc.Row([
                        dbc.Col(html.Iframe(id='bar-chart', style={'width': '100%', 'height': '400px'}), width=6),
                        dbc.Col(html.Iframe(id='bar-chart2', style={'width': '100%', 'height': '400px'}), width=6)
                    ], className="mt-3")
                ], width=6),
                
                # Right side (Map Graph)
                dbc.Col(html.Iframe(id='us-map', style={'width': '100%', 'height': '700px'}), width=6)
            ], className="mt-3")
        ], width=9)
    ], align="start", className="mt-2")
], fluid=True)

# =================================================
# 11. Callback: Update charts based on filters
# =================================================
def update_cause_filter(selected_values):
    if 'ALL' in selected_values:
        return [opt['value'] for opt in cause_options[1:]] if len(selected_values) == 1 else []
    return selected_values

def update_state_filter(selected_values):
    if 'ALL' in selected_values:
        return [opt['value'] for opt in state_options[1:]] if len(selected_values) == 1 else []
    return selected_values

@app.callback(
    [
        Output('bar-chart', 'srcDoc'),
        Output('bar-chart2', 'srcDoc'),
        Output('time-series', 'srcDoc'),
        Output('us-map', 'srcDoc'),
        Output('total-deaths', 'children'),
        Output('avg-deaths', 'children'),
        Output('growth-rate', 'children'),
        Output("police-button", "color"),
        Output("canine-button", "color")
    ],
    [
        Input('year-filter', 'value'),
        Input('cause-filter', 'value'),
        Input('state-filter', 'value'),
        Input('police-button', 'n_clicks'),
        Input('canine-button', 'n_clicks')
    ]
)
def render_dashboard(year_filter, cause_filter, state_filter, police_clicks, canine_clicks):
    police_active = police_clicks % 2 == 1
    canine_active = canine_clicks % 2 == 1

    filtered_data = data.copy()
    
    start_year, end_year = year_filter
    filtered_data = filtered_data[
        (filtered_data['year'] >= start_year) & 
        (filtered_data['year'] <= end_year)
    ]

    if 'ALL' not in cause_filter:
        filtered_data = filtered_data[filtered_data['cause_short'].isin(cause_filter)]

    if 'ALL' not in state_filter:
        filtered_data = filtered_data[filtered_data['state'].isin(state_filter)]

    if police_active and not canine_active:
        filtered_data = filtered_data[filtered_data['canine'] == False]
    elif canine_active and not police_active:
        filtered_data = filtered_data[filtered_data['canine'] == True]
    elif not police_active and not canine_active:
        return "", "", "", "", "0", "0", "0", "secondary", "secondary"

    if filtered_data.empty:
        return "", "", "", "", "0", "0", "0", "secondary", "secondary"

    # Compute summary stats
    total_deaths, avg_per_year, year_change = compute_summary_stats(filtered_data)

    # Prepare data for charts
    cause_data = (
        filtered_data
        .groupby('cause_short', as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
    )

    dept_data = (
        filtered_data
        .groupby('dept', as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
    )

    time_series_data = (
        filtered_data
        .groupby('year', as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
    )

    # Build charts
    bar_chart_obj = create_bar_chart(cause_data.sort_values(by='Count', ascending=False).head(10), 'Count', 'cause_short', 'Top 10 death causes')
    bar_chart_obj_2 = create_bar_chart(dept_data.sort_values(by='Count', ascending=False).head(10), 'Count', 'dept', 'Top 10 departments')
    time_series_obj = create_time_series(time_series_data, 'year', 'Count', 'Deaths Over Time')
    us_map_obj = create_us_heatmap(filtered_data)

    # Convert Altair charts to HTML
    bar_chart_html = bar_chart_obj.to_html() if bar_chart_obj else ""
    bar_chart2_html = bar_chart_obj_2.to_html() if bar_chart_obj_2 else ""
    time_series_html = time_series_obj.to_html() if time_series_obj else ""
    us_map_html = us_map_obj.to_html() if us_map_obj else ""

    police_color = "primary" if police_active else "secondary"
    canine_color = "primary" if canine_active else "secondary"

    return bar_chart_html, bar_chart2_html, time_series_html, us_map_html, str(total_deaths), str(round(avg_per_year, 2)), f"{round(year_change, 2)}%", police_color, canine_color


def update_year_display(year_range):
    return f"Selected Years: {year_range[0]} - {year_range[1]}"
# =================================================
# 12. Launch the app: only open one browser window
# =================================================
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8050")
    # Disable the reloader to avoid opening the browser twice
    app.run_server(debug=True, use_reloader=False)
