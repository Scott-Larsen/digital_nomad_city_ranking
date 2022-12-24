from dash import Dash, html, dcc, Input, Output, dash_table
from itertools import chain
import pandas as pd
import numpy as np


raw_city_stats = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/city_stats.csv')

time_zone_df = pd.read_csv(
    '/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/time_zones.csv')

time_zones = ['GMT ' + time_zone_df['Offset'].astype(
    str) + " " + time_zone_df['City']]

sliders = [["Safety", "safety"],
           ["Cost of Living", "cost_of_living"],
           ["Internet Speed", "internet_speed"]]

app = Dash(__name__)


@app.callback(
    Output('current_datatable', 'children'),
    Input('safety', 'value'),
    Input('cost_of_living', 'value'),
    Input('internet_speed', 'value'),
)
def update_data_table_with_ranking_factors(safety, cost_of_living, internet_speed, max_rows=10):
    weighted_city_stats = raw_city_stats.copy()
    weighted_city_stats.loc[:, 'Weighted Score'] = np.average(
        a=weighted_city_stats.iloc[:, 1:], axis=1, weights=[safety, cost_of_living, internet_speed]).round(2)
    sorted_weighted_city_stats = weighted_city_stats.sort_values(
        'Weighted Score', ascending=False)
    sorted_weighted_city_stats.insert(
        0, 'Rank', sorted_weighted_city_stats.index + 1)
    # sorted_weighted_ranked_city_stats = sorted_weighted_city_stats

    return dash_table.DataTable(sorted_weighted_city_stats.to_dict('records'), [{"name": i, "id": i} for i in sorted_weighted_city_stats.columns],
                                style_cell={'textAlign': 'left', }
                                # 'border': '10%'},
                                )
    # return html.Table([
    #     html.Thead(
    #         html.Tr([html.Th(col)
    #                 for col in sorted_weighted_city_stats.columns])
    #     ),
    #     html.Tbody([
    #         html.Tr([
    #             html.Td(sorted_weighted_city_stats.iloc[i][col]) for col in sorted_weighted_city_stats.columns
    #         ]) for i in range(min(len(sorted_weighted_city_stats), max_rows))
    #     ])
    # ])


def populate_slider(label, input_id):

    return html.Div(children=[
        html.Label(label),
        dcc.Slider(
            id=input_id,
            min=0,
            max=10,
            marks={i: f'{i}Important' if i ==
                   10 else str(i) for i in range(0, 11)},
            value=5,
        ),
    ], style={'padding': 10, 'flex': 2}),


def populate_sliders(sliders):

    return [populate_slider(label=slider[0], input_id=slider[1])[0]
            for slider in sliders]

# TODO: Flight Cost?


app.layout = html.Div([
    html.H1(children='Digital Nomad City Picker'),

    html.Div(children=[


        html.Div(children=[
             html.Label('Company Time Zone'),
             dcc.Dropdown(options=time_zones[0], value='GMT -5 New York'),]),
        # ], style={'padding': 10, 'flex': 2}),

        html.Div(populate_sliders(sliders=sliders)),

    ]),

    html.Div(id='current_datatable',
             #  dcc.Input(style={"margin": "10%"}),
             ),

])


if __name__ == '__main__':
    app.run_server(debug=True)


# app.layout = html.Div([
#     html.H4(children='Remote City Picker'),
#     # html.Div(children=# html.Div(children=[
#              #     html.Label('Company Time Zone'),
#              #     dcc.Dropdown(options=time_zones[0], value='GMT -5 New York')
#              # ], style={'padding': 10, 'flex': 2}),


#              # populate_slider(label="Safety", id="safety"),
#              populate_sliders(sliders)             # # html.Div(children=[
#              # #     html.Label('Safety'),
#              # #     dcc.Slider(
#              # #         id='safety',
#              # #         min=0,
#              # #         max=10,
#              # #         marks={i: f'{i}Important' if i ==
#              # #                10 else str(i) for i in range(0, 11)},
#              # #         value=5,
#              # #     ),
#              # # ], style={'padding': 10, 'flex': 2}),


#              # populate_slider(label="Cost of Living", id="cost_of_living"),

#              # # html.Div(children=[
#              # #     html.Label('Cost of Living'),
#              # #     dcc.Slider(
#              # #         id='cost_of_living',
#              # #         min=0,
#              # #         max=10,
#              # #         marks={i: f'{i}Important' if i ==
#              # #                10 else str(i) for i in range(0, 11)},
#              # #         value=5,
#              # #     ),
#              # # ], style={'padding': 10, 'flex': 2}),

#              # populate_slider(label="Internet Speed", id="internet_speed"),

#              # html.Div(children=[
#              #     html.Label('Internet Speed'),
#              #     dcc.Slider(
#              #         id='internet_speed',
#              #         min=0,
#              #         max=10,
#              #         marks={i: f'{i}Important' if i ==
#              #                10 else str(i) for i in range(0, 11)},
#              #         value=5,
#              #     ),
#              # ], style={'padding': 10, 'flex': 2}),
#              , style={'display': 'flex', 'flex-direction': 'row'}),

#     html.Div(id='current_datatable')

# ])
