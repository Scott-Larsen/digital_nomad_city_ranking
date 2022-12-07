from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np

df = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/city_stats.csv')

time_zone_df = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/time_zones.csv')

time_zones = ['GMT ' + time_zone_df['Offset'].astype(
    str) + " " + time_zone_df['City']]


app = Dash(__name__)


@app.callback(
    Output('current_datatable', 'data'),
    Input('safety', 'value'),
    Input('timezone', 'value'),
    Input('COL', 'value'),
)
def update_data_table_with_ranking_factors(safety, timezone, COL):
    print(df)

    print("printing df.loc[:]")
    print(df.iloc[:, 1:])
    df.loc[:, 'Score'] = np.average(
        a=df.iloc[:, 1:], axis=1, weights=[safety, timezone, COL])
    print(df)
    return df.sort_values('Score', ascending=False)


updated_datatable = update_data_table_with_ranking_factors(2, 3, 1)


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
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
            html.Label('Timezone'),
            dcc.Slider(
                id='timezone',
                min=0,
                max=10,
                marks={i: f'Label {i}' if i ==
                       0 else str(i) for i in range(0, 10)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),

        html.Div(children=[
            html.Label('Safety'),
            dcc.Slider(
                id='safety',
                min=0,
                max=10,
                marks={i: f'Label {i}' if i ==
                       0 else str(i) for i in range(0, 10)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),


        html.Div(children=[
            html.Label('Cost of Living'),
            dcc.Slider(
                id='COL',
                min=0,
                max=10,
                marks={i: f'Label {i}' if i ==
                       0 else str(i) for i in range(0, 10)},
                value=5,
            ),
        ], style={'padding': 10, 'flex': 2}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(generate_table(updated_datatable))

])

if __name__ == '__main__':
    app.run_server(debug=True)
