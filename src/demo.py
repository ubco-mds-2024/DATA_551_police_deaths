import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
import webbrowser
import plotly.express as px
import dash.dash_table as dt
import warnings
from dash import State, callback_context

warnings.simplefilter(action='ignore', category=FutureWarning)


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
app = dash.Dash(__name__, title="Police Officer Deaths Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    """Computes total deaths, average per year, and deaths in recent time periods."""
    if filtered_data.empty:
        return 0, 0, 0, 0, 0

    total_deaths = len(filtered_data)
    year_min = filtered_data['year'].min()
    year_max = filtered_data['year'].max()

    # If the dataset contains only one year, avoid division by zero
    year_span = max(1, year_max - year_min + 1)
    avg_per_year = total_deaths / year_span

    # Dynamically determine the latest year from the filtered data
    current_year = year_max

    # Calculate deaths within specific periods based on available data
    deaths_last_year = filtered_data[filtered_data['year'] == (current_year - 1)].shape[0] if current_year - 1 >= year_min else 0
    deaths_last_5_years = filtered_data[filtered_data['year'] >= max(year_min, current_year - 5)].shape[0]
    deaths_last_10_years = filtered_data[filtered_data['year'] >= max(year_min, current_year - 10)].shape[0]

    return total_deaths, avg_per_year, deaths_last_year, deaths_last_5_years, deaths_last_10_years

# =================================================
# 7. Chart-building and table-building helper functions
# =================================================
def create_bar_chart(data, x_col, y_col, title, y_axis_label="Category"):
    """Builds a bar chart with a custom Y-axis label and comma-formatted tooltips."""
    if data.empty:
        return None

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(x_col, title="Count"),
            y=alt.Y(y_col, title=y_axis_label, sort='-x'),  # Custom Y-axis label
            color=alt.Color(y_col, legend=None),
            tooltip=[
                alt.Tooltip(x_col, title="Count", format=","),
                alt.Tooltip(y_col, title=y_axis_label)
            ]
        )
        .properties(title=title, width=230, height=300)
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
            x=alt.X(x_col, title='Year', axis=alt.Axis(format='d', tickMinStep=5)),
            y=alt.Y(y_col, title='Number of Deaths'),
            tooltip=[
                alt.Tooltip(x_col, title="Year"),
                alt.Tooltip(y_col, title="Deaths", format=",")
            ]
        )
        .properties(title=title, width=800, height=300)
    )
    return chart


def create_us_heatmap(filtered_data):
    """Creates a U.S. choropleth map where non-selected states remain visible in gray."""
    # Count occurrences of each state (for coloring)
    state_counts = filtered_data["state"].value_counts().reset_index()
    state_counts.columns = ["state", "count"]
    state_counts["state"] = state_counts["state"].str.strip()

    # Create a DataFrame with all states, ensuring unselected ones are visible
    all_states = pd.DataFrame({"state": list(state_abbrev_to_fips.keys())})
    state_counts = all_states.merge(state_counts, on="state", how="left").fillna(0)

    # Define the original red color scale
    color_scale = [
        (0, "lightgray"),  # Unselected states in gray
        (0.2, "#fee5d9"),  # Light red
        (0.4, "#fcae91"),  # Soft red
        (0.6, "#fb6a4a"),  # Medium red
        (0.8, "#de2d26"),  # Darker red
        (1, "#a50f15")  # Deep red for high values
    ]

    # Create the choropleth map
    fig = px.choropleth(
        state_counts,
        locations="state",
        locationmode="USA-states",
        color="count",
        color_continuous_scale=color_scale,  # Use the improved red gradient
        scope="usa",
        title="Mapping Fallen Officers: U.S. Deaths by State",
        hover_data={"state": True, "count": True},
    )

    # Set hover template explicitly
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Deaths: %{z}<extra></extra>",
        marker=dict(line=dict(color='black', width=0.5))  # Add borders to states
    )

    # Optimize layout: Disable zooming and panning
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            showcountries=False,
            showland=True,
            landcolor="white",
            projection=dict(
                type="albers usa",
                scale=1.05 if len(state_counts) > 10 else 1.2  # Adjust zoom based on selected states
            ),
            center={"lat": 38, "lon": -96}
        ),
        dragmode=False,
        uirevision="fixed",
        margin={"r": 10, "t": 10, "l": 10, "b": 10},
        height=400,
        title=dict(
            text="Mapping Fallen Officers: U.S. Deaths by State",
            font=dict(size=16),
            x=0.5,
            xanchor="center",
            y=0.95,
            yanchor="top"
        )
    )

    return fig

def create_recent_officer_table(filtered_data):
    """Creates a table showing the 5 most recently fallen officers."""
    if filtered_data.empty:
        return dt.DataTable(
            columns=[{"name": col, "id": col} for col in ["Person", "Date", "Dept Name", "State", "Cause"]],
            data=[],
            style_table={'width': '100%', 'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        )

    # Get the 5 most recent fallen officers (latest date)
    recent_officers = filtered_data.sort_values(by="date", ascending=False).head(5)

    # Select columns and rename them for display
    recent_officers = recent_officers[["person", "date", "dept_name", "state", "cause_short"]].rename(
        columns={"person": "Person", "date": "Date", "dept_name": "Dept Name", "state": "State", "cause_short": "Cause"}
    )

    # Convert DataFrame to Dash Table
    table = dt.DataTable(
        columns=[{"name": col, "id": col} for col in recent_officers.columns],
        data=recent_officers.to_dict("records"),
        style_table={'width': '100%', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'fontWeight': 'bold', 'textAlign': 'center'},
        style_as_list_view=True
    )

    return table


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

cause_options = [{'label': 'Select/Unselect All', 'value': 'ALL'}] + [{'label': c, 'value': c} for c in sorted(data['cause_short'].unique())]
state_options = [{'label': 'Select/Unselect All', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in sorted(data['state'].unique())]

canine_filter = html.Div([
    html.Label("Select Officer Type:", style={"font-weight": "bold", "margin-right": "10px"}),
    dbc.ButtonGroup([
        dbc.Button("All", id="all-button", color="primary", outline=False, n_clicks=1),
        dbc.Button("Human", id="human-button", color="primary", outline=False, n_clicks=1),
        dbc.Button("Canine", id="canine-button", color="primary", outline=False, n_clicks=1),
    ])
], style={"text-align": "right", "margin-bottom": "10px"})

sidebar = html.Div([
    html.Label("Filter by Year"),
    dcc.RangeSlider(
        id='year-filter',
        min=data['year'].min(),
        max=data['year'].max(),
        marks={i: str(i) for i in range(data['year'].min(), data['year'].max() + 1, 50)},
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

# Section: About Fallen Officers
about_fallen_officers = html.Div([
    dbc.Button(
        "About Fallen Officers", id="about-officers-toggle", color="link", className="mb-2 fw-bold"
    ),
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            html.P("The term 'fallen officers' refers to police officers and K9s who have lost their lives while serving their communities."),
            html.P("These deaths occur under various circumstances, including violent confrontations, vehicular incidents, medical emergencies, and ambush attacks."),
            html.P([
                "According to the ", html.Strong("Officer Down Memorial Page (ODMP)"),
                ", the number of fallen officers has fluctuated over time due to shifts in crime rates, public safety policies, and broader social factors."
            ]),
            html.P("While every loss is tragic, understanding these trends helps in shaping better policies and safety measures for law enforcement personnel."),
            html.Blockquote(
                html.P("When a police officer is killed, it's not an agency that loses an officer, it's an entire nation."),
                className="blockquote text-muted"
            ),
            html.Footer("— Chris Cosgriff, ODMP Founder", className="blockquote-footer")
        ])),
        id="about-officers-collapse", is_open=False
    )
])

# Section: About the Data
about_data = html.Div([
    dbc.Button(
        "About the Data", id="about-data-toggle", color="link", className="mb-2 fw-bold"
    ),
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            html.P([
                "Our dataset consists of approximately ", html.Strong("22,800 records"),
                " documenting police deaths in U.S. history from ", html.Strong("1791 to 2016"), "."
            ]),
            html.P([
                "The data is sourced from the ", html.Strong("Officer Down Memorial Page (ODMP)"),
                ", a project started in 1996 by a college student who later became a police officer."
            ]),
            html.P([
                "This dataset is publicly available on the ", 
                html.A("FiveThirtyEight GitHub repository", href="https://github.com/fivethirtyeight/data", target="_blank"),
                " and was used in their analysis, ", html.Em("“The Dallas Shooting Was Among The Deadliest For Police In U.S. History.”")
            ]),
            html.P("The dataset captures details about fallen officers, including:"),
            html.Ul([
                html.Li(html.Strong("Officer Information:"), " Name, department, and End of Watch (EOW) date."),
                html.Li(html.Strong("Circumstances:"), " Cause of death (detailed and categorized)."),
                html.Li(html.Strong("Location:"), " State and year of incident."),
                html.Li(html.Strong("Canine Officers:"), " A flag to identify cases involving police dogs (K9s).")
            ])
        ])),
        id="about-data-collapse", is_open=False
    )
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
    dcc.Markdown("""
        <style>
            .card { height: 100%; }
            .card-body { display: flex; flex-direction: column; justify-content: center; align-items: center; }
        </style>
    """, dangerously_allow_html=True),

    # Title and Buttons at the Top
    dbc.Row([
        dbc.Col(html.H1("Police Officer Deaths Dashboard"), width=9),
        dbc.Col(canine_filter, width=3, style={"text-align": "right"})
    ], align="center", className="mb-3"),

    # Main Layout: Sidebar (Filters + Footer) on Left, Charts on Right
    dbc.Row([
        # Left Sidebar: Filters + Footer
        dbc.Col([
            sidebar,  # Existing filters
            html.Hr(),  # Separator line
            about_fallen_officers,
            html.Hr(),  # Separator line
            about_data    # Footer Section (Collapsible Buttons)
        ], width=2, style={"border-right": "1px solid #ccc", "padding-right": "12px"}),

        # Right Side: Stats + Charts
        dbc.Col([
            # Summary Statistics Row
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H2(id="total-deaths", className="text-center fw-bold"),  
                        html.P([html.Strong("TOTAL DEATHS"), html.Br(), "Selected Period"],  
                            className="text-center text-muted mb-0")
                    ], className="d-flex flex-column justify-content-center align-items-center")
                ], className="h-100 shadow-sm"), width={"xs": 12, "sm": 6, "md": 3, "lg": 2}),  

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H2(id="avg-deaths", className="text-center fw-bold"),
                        html.P([html.Strong("AVG. DEATHS"), html.Br(), "Per Year", html.Br(), "Selected Period"],  
                            className="text-center text-muted mb-0")
                    ], className="d-flex flex-column justify-content-center align-items-center")
                ], className="h-100 shadow-sm"), width={"xs": 12, "sm": 6, "md": 3, "lg": 2}),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H2(id="deaths-last-10", className="text-center fw-bold"),
                        html.P(["Deaths", html.Br(), html.Strong("LAST 10 YEARS"), html.Br(), "of Selection"],  
                            className="text-center text-muted mb-0")
                    ], className="d-flex flex-column justify-content-center align-items-center")
                ], className="h-100 shadow-sm"), width={"xs": 12, "sm": 6, "md": 3, "lg": 2}),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H2(id="deaths-last-5", className="text-center fw-bold"),
                        html.P(["Deaths", html.Br(), html.Strong("LAST 5 YEARS"), html.Br(), "of Selection"],  
                            className="text-center text-muted mb-0")
                    ], className="d-flex flex-column justify-content-center align-items-center")
                ], className="h-100 shadow-sm"), width={"xs": 12, "sm": 6, "md": 3, "lg": 2}),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H2(id="deaths-last-year", className="text-center fw-bold"),
                        html.P(["Deaths", html.Br(), html.Strong("LAST YEAR"), html.Br(), "of Selection"],  
                            className="text-center text-muted mb-0")
                    ], className="d-flex flex-column justify-content-center align-items-center")
                ], className="h-100 shadow-sm"), width={"xs": 12, "sm": 6, "md": 3, "lg": 2})
            ], className="mb-3 align-items-stretch"),

            # Charts Row
            dbc.Row([
                # Left Side: Time Series & Bar Charts
                dbc.Col([
                    html.Iframe(id='time-series', style={'width': '100%', 'height': '400px'}),
                    dbc.Row([
                        dbc.Col(html.Iframe(id='bar-chart', style={'width': '100%', 'height': '400px'}), width=6),
                        dbc.Col(html.Iframe(id='bar-chart2', style={'width': '100%', 'height': '400px'}), width=6)
                    ], className="mt-3")
                ], width=7),

                # Right Side: US Map & Officer Table
                dbc.Col([
                    html.Iframe(id='us-map', style={'width': '100%', 'height': '450px'}),
                    html.Div(id="recent-officer-section")
                ], width=5)
            ], className="mt-3")
        ], width=10)  # Main content should take up most of the space
    ], align="start", className="mt-2", style={"padding-bottom": "15px"})
], fluid=True)

# =================================================
# 11. Callback: Update charts based on filters
# =================================================
from dash.exceptions import PreventUpdate

# def update_officer_type(all_clicks, human_clicks, canine_clicks):
#     all_active = all_clicks % 2 == 1
#     human_active = human_clicks % 2 == 1
#     canine_active = canine_clicks % 2 == 1

#     if all_active:
#         return "primary", "secondary", "secondary"
#     elif human_active:
#         return "secondary", "primary", "secondary"
#     elif canine_active:
#         return "secondary", "secondary", "primary"
#     else:
#         return "secondary", "secondary", "secondary"

@app.callback(
    Output('cause-filter', 'value'),
    Input('cause-filter', 'value'),
    prevent_initial_call=True
)
def update_cause_filter(selected_values):
    """Handles 'Select All' for cause-filter."""
    all_options = [opt['value'] for opt in cause_options[1:]]  # Exclude "Select All"

    if 'ALL' in selected_values:
        if len(selected_values) == 1:  # If only "Select All" is selected, select all causes
            return all_options
        else:  # If "Select All" was unchecked, unselect everything
            return []

    return selected_values



@app.callback(
    Output('state-filter', 'value'),
    Input('state-filter', 'value'),
    prevent_initial_call=True
)
def update_state_filter(selected_values):
    """Handles 'Select All' for state-filter."""
    all_options = [opt['value'] for opt in state_options[1:]]  # Exclude "Select All"

    if 'ALL' in selected_values:
        if len(selected_values) == 1:  # If only "Select All" is selected, select all states
            return all_options
        else:  # If "Select All" was unchecked, unselect everything
            return []

    return selected_values

@app.callback(
    Output("about-officers-collapse", "is_open"),
    Input("about-officers-toggle", "n_clicks"),
    State("about-officers-collapse", "is_open")
)
def toggle_about_officers(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("about-data-collapse", "is_open"),
    Input("about-data-toggle", "n_clicks"),
    State("about-data-collapse", "is_open")
)
def toggle_about_data(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    [
        Output('bar-chart', 'srcDoc'),
        Output('bar-chart2', 'srcDoc'),
        Output('time-series', 'srcDoc'),
        Output('us-map', 'srcDoc'),
        Output('total-deaths', 'children'),
        Output('avg-deaths', 'children'),
        Output('deaths-last-year', 'children'),
        Output('deaths-last-5', 'children'),
        Output('deaths-last-10', 'children'),
        Output("all-button", "color"),
        Output("human-button", "color"),
        Output("canine-button", "color"),
        Output("recent-officer-section", "children")
    ],
    [
        Input('year-filter', 'value'),
        Input('cause-filter', 'value'),
        Input('state-filter', 'value'),
        Input('all-button', 'n_clicks'),
        Input('human-button', 'n_clicks'),
        Input('canine-button', 'n_clicks'),
    ],
    [
        State("all-button", "color"),
        State("human-button", "color"),
        State("canine-button", "color"),
    ]
)

def render_dashboard(year_filter, cause_filter, state_filter, all_clicks, human_clicks, canine_clicks, all_color, human_color, canine_color):
    all_clicks = all_clicks or 0
    human_clicks = human_clicks or 0
    canine_clicks = canine_clicks or 0

    filtered_data = data.copy()

    start_year, end_year = year_filter
    filtered_data = filtered_data[
        (filtered_data['year'] >= start_year) & 
        (filtered_data['year'] <= end_year)
    ]

    # If no causes are selected, return an empty dataset
    if not cause_filter or len(cause_filter) == 0:
        filtered_data = pd.DataFrame(columns=data.columns)
    else:
        filtered_data = filtered_data[filtered_data["cause_short"].isin(cause_filter)]

    # If no states are selected, return an empty dataset
    if not state_filter or len(state_filter) == 0:
        filtered_data = pd.DataFrame(columns=data.columns)
    else:
        filtered_data = filtered_data[filtered_data["state"].isin(state_filter)]



    # Get the ID of the last clicked button
    ctx = callback_context
    if not ctx.triggered:
        last_clicked = "all-button"  # Default selection is All
    else:
        last_clicked = ctx.triggered[0]["prop_id"].split(".")[0]  # Extract button ID

    # Logic for correct selection:
    if last_clicked == "all-button":
        all_active, human_active, canine_active = True, True, True  # Enable all
    elif last_clicked == "human-button":
        all_active, human_active, canine_active = False, True, False  # Only Human
    elif last_clicked == "canine-button":
        all_active, human_active, canine_active = False, False, True  # Only Canine
    else:
        all_active, human_active, canine_active = True, True, True  # Default: All on

    # Apply officer type filter
    if not all_active:  
        if human_active:
            filtered_data = filtered_data[filtered_data["canine"] == False]  # Only human officers
        elif canine_active:
            filtered_data = filtered_data[filtered_data["canine"] == True]  # Only canine officers

    if filtered_data.empty:
        return "", "", "", "", "0", "0", "0", "0", "0", "secondary", "secondary", "secondary", ""

    # Compute summary stats using the latest year in the filtered dataset
    total_deaths, avg_per_year, deaths_last_year, deaths_last_5, deaths_last_10 = compute_summary_stats(filtered_data)

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
    bar_chart_obj = create_bar_chart(
        cause_data.sort_values(by='Count', ascending=False).head(10),
        'Count', 'cause_short', 'Top 10 Death Causes', y_axis_label="Cause of Death"
    )

    bar_chart_obj_2 = create_bar_chart(
        dept_data.sort_values(by='Count', ascending=False).head(10),
        'Count', 'dept', 'Top 10 Departments', y_axis_label="Department"
    )
    time_series_obj = create_time_series(time_series_data, 'year', 'Count', 'Deaths Over Time')
    us_map_obj = create_us_heatmap(filtered_data)

    # Get the table of the most recent fallen officers
    recent_officer_table = create_recent_officer_table(filtered_data)

    # Convert Altair charts to HTML
    bar_chart_html = bar_chart_obj.to_html() if bar_chart_obj else ""
    bar_chart2_html = bar_chart_obj_2.to_html() if bar_chart_obj_2 else ""
    time_series_html = time_series_obj.to_html() if time_series_obj else ""
    us_map_html = us_map_obj.to_html() if us_map_obj else ""

    # Ensure the button colors reflect the selection
    all_color = "primary" if all_active else "secondary"
    human_color = "primary" if human_active else "secondary"
    canine_color = "primary" if canine_active else "secondary"

    recent_officer_section = html.Div([
    html.H5("Most Recently Fallen Officers (Filtered View)", style={"text-align": "center", "margin-top": "0px"}),
    recent_officer_table
    ]) if not filtered_data.empty else ""  # Hide title & table if empty

    return (
        bar_chart_html, bar_chart2_html, time_series_html, us_map_html,
        f"{total_deaths:,}", f"{avg_per_year:,.2f}", f"{deaths_last_year:,}", 
        f"{deaths_last_5:,}", f"{deaths_last_10:,}", all_color, human_color, canine_color, recent_officer_section
    )

def update_year_display(year_range):
    return f"Selected Years: {year_range[0]} - {year_range[1]}"


# =================================================
# 12. Launch the app: only open one browser window
# =================================================
server = app.server  
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050)
