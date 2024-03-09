# Taller 5 - ACTD

import dash
from dash import dcc  # dash core components
from dash import html  # dash html components
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H3("Producto Toma de Decisiones - Productividad en Manufactura"),
        html.H6("Objetivo del Producto", style={'fontWeight': 'bold'}),
        html.H6("El Producto busca estimar la productividad real y objetivo de un proceso de manufactura considerando las siguientes variables explicativas: equipo, departamento, incentivos y tiempo extra.", style={'fontSize': '18px'}),
        html.H6("Instrucciones de uso", style={'fontWeight': 'bold'}),
        html.H6("Seleccione el equipo y el departamento de interés a partir de las listas.", style={'fontSize': '18px'}),
        html.H6("Ingrese el valor del tiempo extra (minutos) de trabajo. En caso de no haber, el valor debe ser 0. [0,15120]", style={'fontSize': '18px'}),
        html.H6("Use el slider disponible para elegir el valor del incentivo en unidades monetarias. En caso de no haber, el valor debe ser 0. [0,150]", style={'fontSize': '18px'})
    ], style={'margin-bottom': '20px'}),
    html.Hr(),
    html.Div(html.H6("Inicio de la Aplicación", style={'fontWeight': 'bold'})),
    html.Div([
        html.H6("Incentivo", style={'fontSize': '18px'}),
        dcc.Slider(
            id='incentivo',
            min=0,
            max=150,
            value=0,
            step=None,
            tooltip={"always_visible": True} 
        )
    ]),
    html.Div([
        html.H6("Tiempo extra", style={'fontSize': '18px'}),
        dcc.Input(
            id='tiempo',
            value=0,
            type='number',
            style={'width': '150px'}
        )
    ]),
    html.Div([
        html.H6("Equipo", style={'fontSize': '18px'}),
        dcc.Dropdown(
            options=[
                {'label': str(i), 'value': i} for i in range(1, 13)
            ],
            value=1,
            id='equipo',
            style={'width': '150px'}
        )
    ]),
    html.Div([
        html.H6("Departamento", style={'fontSize': '18px'}),
        dcc.Dropdown(
            options=[
                {'label': 'Finishing', 'value': 0},
                {'label': 'Sweing', 'value': 1}
            ],
            value=1,
            id='departamento',
            style={'width': '150px'}
        )
    ]),
    html.Hr(),
    html.Div(html.Div(html.H6("Resultados Preliminares la Aplicación", style={'fontWeight': 'bold'}))),
    html.Div(html.Br()),
    html.Div(html.Div(html.H6("Modelo de productividad real", style={'fontWeight': 'bold'}))),
    html.Div(id='output-container99',style={'fontSize': '20px'}),
    html.Hr(),
    html.Div(html.Div(html.H6("Resultados de la Aplicación", style={'fontWeight': 'bold'}))),
    html.Div(id='output-container',style={'fontSize': '20px'}),
    html.Div(id='output-container2',style={'fontSize': '20px'})
])

import plotly.graph_objs as go

@app.callback(
    Output('output-container99', 'children'),
    [
        Input('incentivo', 'value'),
        Input('tiempo', 'value'),
        Input('equipo', 'value'),
        Input('departamento', 'value')
    ]
)
def update_output(incentivo, tiempo, equipo, departamento):
    betas_real = [0.794920, -0.185258, -0.018902, -0.003449, 0.004133, -0.032679, 
         -0.062889, -0.054918, -0.051835, -0.051450, -0.045606, -0.061901, 
         -0.021129, -0.000005, 0.004122]
    
    betas_target = [0.731224, -0.089341, 0.012373, 0.014434, -0.002691, -0.022166, 
               0.025077, 0.016419, 0.006372, 0.038684, 0.024695, 0.002289, 
               0.045522, -0.000003, 0.001895]
    
    if tiempo == "":
        tiempo = 0
    
    coeficientes = [1, departamento, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, tiempo, incentivo]
    
    for i in range(1, 14):
        if equipo == i and equipo != 1:
            coeficientes[i] = 1
    
    vector_efectos_real = [betas_real[i] * coeficientes[i] for i in range(15)]
    
    vector_efectos_target = [betas_target[i] * coeficientes[i] for i in range(15)]
    
    x_data = ['Intercepto', 'Departamento', 'Equipo 2', 'Equipo 3', 'Equipo 4',
              'Equipo 5', 'Equipo 6', 'Equipo 7', 'Equipo 8', 'Equipo 9',
              'Equipo 10', 'Equipo 11', 'Equipo 12', 'Tiempo extra', 'Incentivo']
    
    bar_plot_real = go.Bar(x=x_data, y=vector_efectos_real, name='Productividad Real', marker=dict(color='blue'))
    
    bar_plot_target = go.Bar(x=x_data, y=vector_efectos_target, name='Productividad Objetivo', marker=dict(color='red'))
    
    layout = go.Layout(title='Efectos de los parámetros en la productividad', xaxis=dict(title='Variables'), yaxis=dict(title='Efectos'))
    fig = go.Figure(data=[bar_plot_real, bar_plot_target], layout=layout)
    
    return dcc.Graph(figure=fig)


@app.callback(
    Output('output-container', 'children'),
    [
        Input('incentivo', 'value'),
        Input('tiempo', 'value'),
        Input('equipo', 'value'),
        Input('departamento', 'value')
    ]
)
def update_output(incentivo, tiempo, equipo, departamento):
    betas = [0.794920, -0.185258, -0.018902, -0.003449, 0.004133, -0.032679, 
         -0.062889, -0.054918, -0.051835, -0.051450, -0.045606, -0.061901, 
         -0.021129, -0.000005, 0.004122]
    if tiempo=="":
        tiempo=0
    coeficientes=[1,departamento,0,0,0,0,0,0,0,0,0,0,0,tiempo,incentivo]
    for i in range(1,13):
        if equipo==i and equipo!=1:
            coeficientes[i+1]=1
            
    productividad_real=sum(betas * coeficientes for betas, coeficientes in zip(betas, coeficientes))
    
    respuesta3 = html.P("La productividad real para los parámetros dados es: " + str(min(round(productividad_real,2),1)),style={'color': 'blue'})

    return respuesta3

@app.callback(
    Output('output-container2', 'children'),
    [
        Input('incentivo', 'value'),
        Input('tiempo', 'value'),
        Input('equipo', 'value'),
        Input('departamento', 'value')
    ]
)
def update_output2(incentivo, tiempo, equipo, departamento):        
    betas_target=[0.731224, -0.089341, 0.012373, 0.014434, -0.002691, -0.022166, 
               0.025077, 0.016419, 0.006372, 0.038684, 0.024695, 0.002289, 
               0.045522, -0.000003, 0.001895]
    if tiempo=="":
        tiempo=0
    coeficientes_target=[1,departamento,0,0,0,0,0,0,0,0,0,0,0,tiempo,incentivo]
    for i in range(1,13):
        if equipo==i and equipo!=1:
            coeficientes_target[i+1]=1
            
    productividad_target=sum(betas_target * coeficientes_target for betas_target, coeficientes_target in zip(betas_target, coeficientes_target))
    
    respuesta4 = html.P("La productividad objetivo o meta para los parámetros dados es: " + str(min(round(productividad_target,2),1)), style={'color': 'red'})

    return respuesta4

if __name__ == '__main__':
    app.run_server(debug=True)
