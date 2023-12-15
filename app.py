import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import numpy as np
from df_preparation import ecom_sales
from components import create_logo

app = dash.Dash()

logo_link = "https://images.unsplash.com/photo-1629101098327-fd543a15adbf?q=80&w=2148&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"


# GRAPH SANS CALLBACK (SANS FILTRE)

# Graph1
ecom_sales_1 = ecom_sales.groupby(['Country'])['Quantity'].agg(
    'sum').reset_index(name='Total Sales')
bar_graph = px.bar(
    data_frame=ecom_sales_1,
    x='Total Sales',
    y='Country',
    title='Total Sales by Country',
    orientation='h',
    color="Country"
)

# Graph2
line_graph = px.line(
    data_frame=ecom_sales_1,
    x='Country',
    y='Total Sales',
    title='Total Sales by Country',
)

# Graph3
df_pays = ecom_sales.groupby(['Country']).size().reset_index(
    name='total').sort_values(by='total', ascending=False).reset_index(drop=True)
# print(df_pays.loc[0]['total'])
df_graph = px.bar(
    data_frame=df_pays,
    x='total',
    y='Country',
    color='Country'
)
df_graph.update_layout({
    'yaxis': {'dtick': 1,
              'categoryorder': "total ascending"},
    'paper_bgcolor': 'rgb(224, 255, 252)'
})

logo = html.Img(
    src=logo_link,
    style={
        'height': "80px",
        "width": "80px", }
)
# LAYOUT
# #AA63FA
app.layout = html.Div(
    style={'margin': 0, 'box-sizing': 'border-box', 'color': '#573156'},
    children=[
        html.Div(
            style={'background-color': '#573156',
                   'color': 'white',
                   'margin': 0, "padding": "6px"},
            children=[logo]
        ),
        html.Div(
            style={'text-align': 'center',
                   'font-size': 22, 'background-color': "#F1F1F1",
                   'margin': 0, 'padding': 24},
            children=[
                html.H1('DASHBOARD'),
                html.Span(
                    style={'margin': 'auto'},
                    children=[
                        f"Prepared: {datetime.now().date().strftime('%d %b %Y')}",
                        html.Br(),
                        " by ",
                        html.B('Caroline Zumbiehl, '),
                        html.Br(),
                        html.I('Data Scientist')
                    ]),
                html.P(
                    style={'margin-top': '15px', 'font-size': "12px"},
                    children=['Choose your welcome sentence...']
                ),
                # dropdown for the welcome sentence
                dcc.Dropdown(
                    id="nothing-why",
                    options=[{'label': 'Greetings', 'value': 'You look so cool today! You are the GOAT ! '},
                             {'label': 'Meteo',
                                 'value': "The weather is rainy today. Don't forget your umbrella !"},
                             {'label': 'Quote', 'value': 'The sky is the limit!'}]
                ),
                html.P(
                    id='nothing',
                    style={'margin-bottom': "22px", 'color': '#D75156'},
                    children=[]),
                # Graph 1
                html.Div(
                    dcc.Graph(
                        id="ecom_bar",
                        figure=bar_graph)
                ),
                # Graph 2
                html.Div(
                    dcc.Graph(
                        id="ecom_line",
                        figure=line_graph)
                ),
                # Graph 3
                html.Div(
                    dcc.Graph(
                        id="df_country",
                        figure=df_graph)
                ),
                # graph 4 avec drop down
                html.Div(
                    children=[
                        html.H2("Ventes par année, sélectionnez un pays:"),
                        dcc.Dropdown(
                            style={'margin': '0px 0px 20px 0px'},
                            id="graph4_dd",
                            options=[
                                {'label': 'UK', 'value': 'United Kingdom'},
                                {'label': 'GM', 'value': 'Germany'},
                                {'label': 'FR', 'value': 'France'},
                                {'label': 'HK', 'value': 'Hong Kong'},
                                {'label': 'AUS', 'value': 'Australia'},
                            ]
                        ),
                        dcc.Graph(
                            id="graph4",
                            figure={})
                    ]
                ),
                # graph 5 avec slider Date
                html.Div(
                    children=[
                        html.H2("Ventes par jour - sélectionnez un jour:"),
                        dcc.DatePickerSingle(
                            id="graph5_pic",
                            min_date_allowed=ecom_sales['date'].min(),
                            max_date_allowed=ecom_sales['date'].max(),
                            date=date(2020, 1, 1),
                            initial_visible_month=date(2020, 1, 1),
                            style={'width': '200px', 'margin': '0 auto'}),
                        dcc.Graph(
                            id="graph5",
                            figure={})
                    ]
                ),
                # graph6 (single Slider = seuil)
                html.Div(
                    children=[
                        html.H2(
                            "Nombre de ventes par catégorie au dessus du seuil"),
                        dcc.Slider(
                            id="graph6_slider",
                            min=ecom_sales['OrderValue'].min(),
                            max=ecom_sales['OrderValue'].max(),
                            value=0,
                            step=50,
                            vertical=False),
                        dcc.Graph(
                            id="graph6",
                            figure={})
                    ]
                ),
            ]
        )
    ])


# CALLBACK pour les graphes avec filtre et autre éléments interactifs

# call back sur la welcome sentence (choix du type de message)
@app.callback(
    Output('nothing', 'children'),
    Input('nothing-why', 'value')
)
def update_plot(selection):
    sentence = "Welcome !"
    if selection:
        sentence = selection
    return html.B(sentence)


# call back sur le graph 4 (choix du pays)
# ventes par années (et par pays)
@app.callback(
    Output('graph4', 'figure'),
    Input('graph4_dd', 'value')
)
def update_country(input_country):
    country = 'All Countries'
    df = ecom_sales.copy(deep=True)
    if input_country:
        country = input_country
        df = df[df['Country'] == input_country]

    df_sort = df.groupby(['year'])['OrderValue'].agg(
        'sum').reset_index(name="total")

    fig = px.line(
        data_frame=df_sort,
        x='year',
        y='total',
        title=f'Ventes par an - {country}'
    )
    return fig


# call back sur le graph 5
# ventes par catégories (et par date)

@app.callback(
    Output('graph5', 'figure'),
    Input('graph5_pic', 'date')
)
def update_date(input_date):
    sales = ecom_sales.copy(deep=True)
    if input_date:
        sales = sales[sales['date'] == input_date]

    df = sales.groupby('category')['OrderValue'].agg(
        'sum').reset_index(name='total')
    fig = px.bar(
        data_frame=df,
        x='total',
        y='category',
        title=f"Vente par catégorie - {input_date}",
        orientation='h'
    )
    return fig


# callback sur graph6
# nombre de ventes par catégorie (au dessus d'un seuil)
@app.callback(
    Output('graph6', 'figure'),
    Input('graph6_slider', 'value')
)
def update_seuil(input_seuil):
    sales = ecom_sales.copy(deep=True)
    if input_seuil:
        sales = sales[sales['OrderValue'] >= input_seuil]

    sales = sales.groupby(['category'])['OrderValue'].size(
    ).reset_index(name='Nombre de ventes')
    fig = px.bar(
        data_frame=sales,
        x='Nombre de ventes',
        y='category',
        title=f"Nombre de vente supérieur à {input_seuil} par catégories"
    )
    return fig


if __name__ == ('__main__'):
    app.run_server(debug=True)
