from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np

raw_city_stats = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/city_stats.csv')

time_zone_df = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/time_zones.csv')

time_zones = ['GMT ' + time_zone_df['Offset'].astype(
    str) + " " + time_zone_df['City']]


app = Dash(__name__)


@app.callback(
    Output('current_datatable', 'children'),
    Input('safety', 'value'),
    Input('COL', 'value'),
    Input('internet_speed', 'value'),
)
def update_data_table_with_ranking_factors(safety, COL, internet_speed, max_rows=10):
    print("printing raw_city_stats.iloc[:]")
    print(raw_city_stats.iloc[:])
    print("printing raw_city_stats.iloc[:, 1:]")
    print(raw_city_stats.iloc[:, 1:])
    weighted_city_stats = raw_city_stats.copy()
    weighted_city_stats.loc[:, 'Score'] = np.average(
        a=weighted_city_stats.iloc[:, 1:], axis=1, weights=[safety, COL, internet_speed]).round(2)
    print(weighted_city_stats)
    sorted_weighted_city_stats = weighted_city_stats.sort_values(
        'Score', ascending=False)
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col)
                    for col in sorted_weighted_city_stats.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(sorted_weighted_city_stats.iloc[i][col]) for col in sorted_weighted_city_stats.columns
            ]) for i in range(min(len(sorted_weighted_city_stats), max_rows))
        ])
    ])

# Have drop-down add columns to the dataframe and calculate a new score column to rank them
# INTERNET SPEED
# Flight Cost


app.layout = html.Div([
    html.H4(children='Remote City Picker'),
    html.Div(children=[
        html.Div(children=[
            html.Label('Company Time Zone'),
            dcc.Dropdown(options=time_zones[0], value='GMT -5 New York')
        ], style={'padding': 10, 'flex': 2}),

        html.Div(children=[
            html.Label('Safety'),
            dcc.Slider(
                id='safety',
                min=0,
                max=10,
                marks={i: f'{i}Important' if i ==
                       10 else str(i) for i in range(0, 11)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),


        html.Div(children=[
            html.Label('Cost of Living'),
            dcc.Slider(
                id='COL',
                min=0,
                max=10,
                marks={i: f'{i}Important' if i ==
                       10 else str(i) for i in range(0, 11)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),

        html.Div(children=[
            html.Label('Internet Speed'),
            dcc.Slider(
                id='internet_speed',
                min=0,
                max=10,
                marks={i: f'{i}Important' if i ==
                       10 else str(i) for i in range(0, 11)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(id='current_datatable')

])

if __name__ == '__main__':
    app.run_server(debug=True)
