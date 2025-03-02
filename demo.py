import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
import webbrowser

# =================================================
# 1. Load the CSV data
# =================================================
file_path = 'clean_data.csv'
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
            x=alt.X(x_col, sort='-y'),
            y=alt.Y(y_col),
            color=alt.Color(x_col, legend=None),
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

def create_us_map(filtered_data):
    """Builds a US map showing death counts by state."""
    if filtered_data.empty:
        return None
    
    # Aggregate number of deaths by state/fips
    state_counts = (
        filtered_data
        .groupby(['state', 'fips'], as_index=False)
        .size()  # creates a column named 'size'
        .rename(columns={'size': 'Deaths'})
    )

    # Drop rows where fips is NaN (meaning the abbreviation didn't match)
    state_counts = state_counts.dropna(subset=['fips'])

    # Load US states topo data
    states = alt.topo_feature(vega_data.us_10m.url, feature='states')

    # Build the map
    map_chart = (
        alt.Chart(states)
        .mark_geoshape()
        .encode(
            color=alt.Color('Deaths:Q', scale=alt.Scale(scheme='blues')),
            tooltip=['state:N', 'Deaths:Q']
        )
        .transform_lookup(
            lookup='id',  # the FIPS code in the topojson
            from_=alt.LookupData(state_counts, 'fips', ['Deaths', 'state'])
        )
        .project('albersUsa')
        .properties(width=500, height=400)
    )
    return map_chart

# =================================================
# 8. Sidebar: user filters
# =================================================
sidebar = html.Div([
    html.Label("Filter by Year"),
    dcc.RangeSlider(
        id='year-filter',
        min=data['year'].min(),
        max=data['year'].max(),
        marks={i: str(i) for i in range(data['year'].min(), data['year'].max()+1, 10)},
        step=1,
        value=[data['year'].min(), data['year'].max()]
    ),
    html.Br(),
    html.Label("Filter by Cause"),
    dcc.Dropdown(
        id='cause-filter',
        options=[{'label': c, 'value': c} for c in sorted(data['cause_short'].unique())],
        multi=True,
        placeholder="Select Cause(s)"
    ),
    html.Br(),
    html.Label("Filter by State"),
    dcc.Dropdown(
        id='state-filter',
        options=[{'label': s, 'value': s} for s in sorted(data['state'].unique())],
        multi=True,
        placeholder="Select State(s)"
    )
])

# =================================================
# 9. Summary stats area
# =================================================
summary_section = html.Div(id='summary-stats')

# =================================================
# 10. Main layout
# =================================================
app.layout = dbc.Container([
    html.H1("Police Officer Deaths Dashboard"),
    dbc.Row([dbc.Col(summary_section, width=12)]),
    dbc.Row([
        dbc.Col(sidebar, width=3),
        dbc.Col(html.Iframe(id='bar-chart', style={'width': '100%', 'height': '400px'}), width=4),
        dbc.Col(html.Iframe(id='time-series', style={'width': '100%', 'height': '400px'}), width=4)
    ]),
    dbc.Row([
        dbc.Col(html.Iframe(id='us-map', style={'width': '100%', 'height': '400px'}), width=6),
        dbc.Col(html.Iframe(id='extra-chart', style={'width': '100%', 'height': '400px'}), width=6)
    ])
], fluid=True)

# =================================================
# 11. Callback: Update charts based on filters
# =================================================
@app.callback(
    [
        Output('bar-chart', 'srcDoc'),
        Output('time-series', 'srcDoc'),
        Output('us-map', 'srcDoc'),
        Output('extra-chart', 'srcDoc'),
        Output('summary-stats', 'children')
    ],
    [
        Input('year-filter', 'value'),
        Input('cause-filter', 'value'),
        Input('state-filter', 'value')
    ]
)
def render_dashboard(year_filter, cause_filter, state_filter):
    # Copy the original data
    filtered_data = data.copy()

    # Filter by year
    start_year, end_year = year_filter
    filtered_data = filtered_data[
        (filtered_data['year'] >= start_year) &
        (filtered_data['year'] <= end_year)
    ]

    # Filter by cause
    if cause_filter:
        filtered_data = filtered_data[filtered_data['cause_short'].isin(cause_filter)]

    # Filter by state
    if state_filter:
        filtered_data = filtered_data[filtered_data['state'].isin(state_filter)]

    # If nothing remains after filtering
    if filtered_data.empty:
        return "", "", "", "", html.H3("No data available for the selected filters.")

    # Compute summary stats
    total_deaths, avg_per_year, year_change = compute_summary_stats(filtered_data)
    summary = html.Div([
        html.P(f"Total Deaths: {total_deaths}"),
        html.P(f"Average Deaths per Year: {round(avg_per_year, 2)}"),
        html.P(f"Annual Growth Rate: {round(year_change, 2)}%")
    ])

    # Prepare data for the bar chart (by cause)
    cause_data = (
        filtered_data
        .groupby('cause_short', as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
    )

    # Prepare data for the time series (by year)
    time_series_data = (
        filtered_data
        .groupby('year', as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
    )

    # Build charts
    bar_chart_obj = create_bar_chart(cause_data, 'cause_short', 'Count', 'Main Causes')
    time_series_obj = create_time_series(time_series_data, 'year', 'Count', 'Deaths Over Time')
    us_map_obj = create_us_map(filtered_data)

    # Convert Altair charts to HTML
    bar_chart_html = bar_chart_obj.to_html() if bar_chart_obj else ""
    time_series_html = time_series_obj.to_html() if time_series_obj else ""
    us_map_html = us_map_obj.to_html() if us_map_obj else ""

    # "extra-chart" is empty
    return bar_chart_html, time_series_html, us_map_html, "", summary

# =================================================
# 12. Launch the app: only open one browser window
# =================================================
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8050")
    # Disable the reloader to avoid opening the browser twice
    app.run_server(debug=True, use_reloader=False)

