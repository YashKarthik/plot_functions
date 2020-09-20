import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
                    html.Br(),
                    dcc.Dropdown(id = 'graph-type',
                                options = [
                                    {'label':'Polynomial','value':'poly'},
                                    {'label':'Trigonometric','value':'trig'},
                                    ],
                                multi = False,
                                value = 'poly',
                                style = {
                                    'background-color':'lightblue',
                                    'border-color':'dimgrey', 'border-radius':'10px',
                                    'font-family':'Arial Rounded MT Bold'}),

                    html.Br(),

                    dcc.Input(id = 'equation', value = 'x', type = 'text'),
                    html.Button(id='eq-submit', n_clicks = 0, children = 'Plot !!!',
                                style = {
                                    'background-color':'lightblue', 'border-radius':'10px'}),

                    html.Div(id = 'output-graph',
                             style = {
                                'overflow':'allow'})
])

@app.callback(
        Output(component_id = 'output-graph', component_property = 'children'),
        [Input(component_id = 'eq-submit', component_property = 'n_clicks')],

        [State('equation', 'value'),
         State('graph-type', 'value')]
)

def update(n__clicks, equation, graph_type):
    equation = equation.replace('^', '**')

    if graph_type == 'trig':
        eq = 'np.'+ equation
        if 'tan' in eq:
            x = np.linspace(-np.pi, np.pi, 200)
        else:
            x = np.linspace(-4*np.pi, 4*np.pi, 2200)

    else:
        x = np.linspace(-50, 50, 5000)
        eq = equation

    y = eval(eq)
    df = pd.DataFrame({
                     'x':x,
                     'y':y})

    return dcc.Graph(
                 id = 'graph',
                 figure={
                     'data': [{
                         'x':df['x'], 'y':df['y'],
                         'type':'line', 'name':equation},
                     ],
                     'layout':{
                         'title':equation
                     }
                 }
            )

if __name__ == '__main__':
    app.run_server(debug = True)
