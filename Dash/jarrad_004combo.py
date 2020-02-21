import os
from pathlib import Path
import dash
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
import dash_daq as daq


IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")
IRP2019_E = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_E")
CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_P")
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_E")




powerlist =list(CSIR_LC_2019_E.columns)
print(powerlist)
removelist=[powerlist[0],powerlist[11],powerlist[13]]
removelist

for i in removelist:
    print(f'remove {i}')
    powerlist.remove(i)


tracebar=[]


colours=["rgb(128, 43, 0)",    # COA
         "rgb(0, 153, 0)",     # NUC
         "rgb(255, 255, 0)",   # GAS
         "rgb(255, 102, 0)",   # PEA
         "rgb(0, 102, 102)",   # HYD
         "rgb(0, 102, 255)",   # WIN
         "rgb(204, 0, 153)",   # CSP
         "rgb(204, 0, 0)",     # SPV
         "rgb(0, 102, 102)",   # DPV
         "rgb(51, 51, 51)",    # BIO
         "rgb(64, 255, 0)",    # PST
]



Dropdown= html.Div([
             dcc.Dropdown(
                    id='Dropdown',
                    options=[
                        {'label': 'Installed capacity [MW]', 'value': "P", },
                        {'label': 'Energy produced [GWh]', 'value': "E", },
 ],
                    value='P',

                    multi=False,
                    ),
            ],)

Powerlayout={
  "title": "<br><br>NYC Car Wrecks",
  # "width": 900,
  "xaxis": {
    "ticks": "",
    "mirror": False,
    "showgrid": True,
    "showline": False,
    "zeroline": False,
    "autorange": True,
    # "gridcolor": "rgb(255, 255, 255)",
    # "linecolor": "rgb(34,34,34)",
    "linewidth": 1
  },
  "yaxis": {
    "type": "linear",
    "ticks": "",
    "title": "Click to enter Y axis title",
    "domain": [0.55, 0.95],
    "mirror": False,
    "showgrid": True,
    "showline": False,
    "zeroline": False,
    "autorange": True,
    # "gridcolor": "rgb(255, 255, 255)",
    # "linecolor": "rgb(34,34,34)",
    "linewidth": 1
  },
  "height": 900,
  "legend": {
    # "x": 1.019163763066202,
    # "y": 0.5147321428571429,
    # "xref": "paper",
    # "yref": "paper",
    # "bgcolor": "rgba(255, 255, 255, 0.5)",
    "traceorder": "normal"
  },
  # "margin": {"l": 100},
  "xaxis2": {
    "type": "linear",
    "ticks": "",
    "title": "<br><br><br>Box Plot Of Wrecks From 2013-2015",
    "anchor": "y2",
    "domain": [0, 1],
    "mirror": False,
    "showgrid": True,
    "showline": False,
    "zeroline": False,
    "autorange": True,
    # "gridcolor": "rgb(255, 255, 255)",
    # "linecolor": "rgb(34,34,34)",
    "linewidth": 1
  },
  "yaxis2": {
    "type": "linear",
    "ticks": "",
    "title": "# Of Wrecks",
    "anchor": "x2",
    "domain": [0.05, .45],
    "mirror": False,
    "showgrid": True,
    "showline": False,
    "zeroline": False,
    "autorange": True,
    # "gridcolor": "rgb(255, 255, 255)",
    # "linecolor": "rgb(34,34,34)",
    "linewidth": 1
  },

  "barmode": "stack",
  "autosize": False,
  "showlegend": True,
}



PowerGraphs= html.Div(
    [dcc.Graph(id="PowerGraphs",figure=dict(data=tracebar,layout=Powerlayout))],
    style={
        #'padding-top': 20,
        'padding-bottom': 20,
        "height": 1300,},
    )






######################### Text GenWind

Text_GenWind =  html.Div([
    dbc.Jumbotron([
        html.H4(children='Power Graph and Rose Chart Display', ),
        html.P(children='Further analysis of the selected point on the map of South Africa is displayed in the power '
                        'graph and rose chart. The selection can be customised using the drop-down menus for hub '
                        'height(s) and turbine(s). This allows for a graphic represent of each of the selected '
                        'criteria.'),
        html.P(children='A normal distribution for each of the hub height’s selected is plotted on the graph. The axis '
                        'on the left estimates the wind probability density percentages based on time series data '
                        'collected. Power curves are plotted over the normal distribution graphs from the turbine '
                        'selections made. The power curve(s) are linked to the right axis and are displayed as power '
                        'generated (kW).'),
        html.P(children='The rose chart to the right of the graph represents the wind direction as a percentage based '
                        'on the hub height(s) selected.'),

        ])
    ],)



years = CSIR_LC_2019_E['Year']




# fill in layout

PieLayout= {"grid": {"rows": 1, "columns": 2},}
PieLayout["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": "2018",
    "plotlycommand": "animate",
    "values": CSIR_LC_2019_E['Year'],
    "visible": True
}
PieLayout["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

PieData = [
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0],
        "domain": {"column": 0},
        "title": f"2018 <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0])/1000))} [unit]",
        "hole": .4,
        "type": "pie",
        "textposition":"inside",
        "scalegroup":'one',
        "marker": {"colors":colours},

    },
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0],
        "title": f"2050 <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0])/1000))} [unit]",
        "domain": {"column": 1},
        "name": "Change",
        "hole": .4,
        "type": "pie",
        "textposition":"inside",
        "scalegroup":'one',
"color":colours,
    }]



# make frames

PieFrames= []
for year in years:
    frame = {"data": [], "name": str(year)}
    # frame["data"].append(go.Pie(labels=powerlist,
    #                             values=np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0],
    #                             textinfo='label+percent',
    #                             textposition='inside',
    #                             scalegroup='one',
    #                             hole=.3,
    #                             domain= {"column": 1},
    #                             ))

    frame["data"]=[
        {
            "labels": powerlist,
            "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0],
            "domain": {"column": 0},
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            "scalegroup": 'one',
            "title": f"2018 <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0]) / 1000))} [unit]",
            "coloraxis":colours,
        },
        {
            "labels": powerlist,
            "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0],
            "domain": {"column": 1},
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            "scalegroup": 'one',
            "title": f"{year} <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0]) / 1000))} [unit]",
            "coloraxis": colours,
        }]


    PieFrames.append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


PieLayout["sliders"] = [sliders_dict]


######################################







PieGraphs= html.Div(
    [dcc.Graph(id="Pie",figure=dict(data=PieData,
                                    layout=PieLayout,
                                    frames=PieFrames))
     ],)




###############################################################################################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(children=[
    html.Div([

        dbc.Row([
            dbc.Col(Text_GenWind,
                    sm=6), ]),
        dbc.Row([
            dbc.Col(Dropdown,
                    sm=5),
            dbc.Col(daq.Slider(id="slider",
                               min=2018,
                               max=2050,
                               step=1,
                               value=2018,
                               marks={'2018': '2018',
                                      '2034': '2034',
                                      '2050': '2050'},
                               handleLabel={"showCurrentValue": True,"label": "VALUE"},
                               included=False,

                               ),
                    sm=5),
            dbc.Col(dbc.Checklist(
                            id="switches",
                            options=[
                                    {"label": "Option 1", "value": True},
                                    ],
                            value=[],
                            switch=True,
            ),

                    sm=2),
            ]),
        dbc.Row(
            dbc.Col(PowerGraphs,
                    sm=8,
                    align="center",
                    width={"offset": 2})
        ),
        dbc.Row(
            dbc.Col(html.Div(
                [dbc.Jumbotron(
                    html.P("this is a Pie Chart")
                )]
            ),
                    sm=8,
                    align="center",
                    width={"offset": 2})
        ),
        dbc.Row(
            dbc.Col(PieGraphs,
                    sm=8,
                    align="center",
                    width={"offset": 2})
        ),
    ]

    )

])

###############################################################################################################################################
@app.callback(Output("PowerGraphs", "figure"),
                [   Input('Dropdown', 'value'),
                    Input('slider', 'value'),
                    Input('switches', 'value'),],
            [
                # State("RadioPower", "value"),
             ],)
def updateMapRSA(DropdownValue,sliderValue,switchesValue):

    # print(f'DropdownValue is {DropdownValue}')
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

#######################################




    if "P"==DropdownValue:
        # print("P")
        DF_IRP=IRP2019_P
        DF_CSIR=CSIR_LC_2019_P
    if "E"==DropdownValue:
        # print("E")
        DF_IRP=IRP2019_E
        DF_CSIR=CSIR_LC_2019_E

    traces = []

    if len(switchesValue)>0: # True

        for i, power in enumerate(powerlist):

            traces.append(
                go.Bar(x=[sliderValue],
                       y=DF_IRP[CSIR_LC_2019_E['Year'] == sliderValue][power],
                       name=power,
                       legendgroup=power,
                       # fillcolor=colours[i],
                       marker=dict(color=colours[i]),
                       )
            )

            traces.append(
                go.Bar(x=[sliderValue],
                       y=DF_CSIR[CSIR_LC_2019_E['Year'] == sliderValue][power],
                       name=power,
                       legendgroup=power,
                       xaxis='x2',
                       yaxis='y2',
                       showlegend=False,
                       marker=dict(color=colours[i]),
                       ))

    else:
        for i, power in enumerate(powerlist):
            traces.append(
                go.Bar(x=DF_IRP['Year'],
                       y=DF_IRP[power],
                       name=power,
                       legendgroup=power,
                       marker=dict(color=colours[i]),
                       )
            )

            traces.append(
                go.Bar(x=DF_IRP['Year'],
                       y=DF_CSIR[power],
                       name=power,
                       legendgroup=power,
                       xaxis='x2',
                       yaxis='y2',
                       showlegend=False,
                       marker=dict(color=colours[i]),
                       ))






    figure = dict(data=traces,layout=Powerlayout)
    return figure


if __name__ == '__main__':
    app.run_server(port=8848,debug=True)

