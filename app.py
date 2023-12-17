import dash
from dash import dcc, html, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import numpy as np
from df_preparation import ecom_sales
import random
# DataTable, FormatTemplate


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


# graph 9 - ventes (x= total, y quantité) par pays avec indicateurs clés

ecom_country = ecom_sales.groupby('Country')['OrderValue'].agg(['sum', 'count']).reset_index(
).rename(columns={'count': 'Sales Volume', 'sum': 'Total Sales ($)'})

ecom_scatter = px.scatter(ecom_country, x='Total Sales ($)', y='Sales Volume',
                          color='Country', width=350, height=400, custom_data=['Country'])
ecom_scatter.update_layout({'legend': dict(orientation='h', y=-0.5, x=1,
                                           yanchor='bottom', xanchor='right'), 'margin': dict(l=20, r=20, t=25, b=0)})


# graph 12 with 2 conditional drop down.
major_categories = list(ecom_sales['Major Category'].unique())
minor_categories = list(ecom_sales['Minor Category'].unique())
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'


# table 14

key_stats_tb = ecom_sales.groupby(['Country', 'Major Category', 'Minor Category'])['OrderValue'].agg(['sum', 'count', 'mean']).reset_index(
).rename(columns={'count': 'Sales Volume', 'sum': 'Total Sales ($)', 'mean': 'Average Order Value ($)'})

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
                # Graph 7 recherche d'un produit - input text
                html.Div(
                    children=[
                        html.H2('Sales by product'),
                        dcc.Input(
                            id="search_prod",
                            type="text",
                            placeholder='Filter Product Description',
                            debounce=True,
                            required=False,
                            style={'width': '200px', 'height': '30px'},
                        ),
                        dcc.Graph(
                            id='search_prod_graph',
                            figure={}),
                    ]
                ),
                # Graph 8 montant de la vente en fonction des quantités avec indication des pays concernés et input range sur les valeurs de ventes
                html.Div(
                    children=[
                        html.H2(
                            'Sales by quantities (and country), selecting a range over a certain value'),
                        dcc.Input(
                            id="graph8_input_range",
                            type="range",
                            min=50,
                            max=550,
                            value=50,
                            debounce=False,
                            required=False,
                            style={'width': '300px', 'height': '30px'},
                        ),
                        dcc.Graph(
                            id='graph8',
                            figure={}),
                    ]
                ),
                # Graph 9 avec impression des statistiques
                html.Div(
                    children=[
                        html.H2('Sales by Country'),
                        dcc.Graph(id='scatter_fig', figure=ecom_scatter)
                    ],
                    style={'width': '350px', 'height': '500px', 'display': 'inline-block',
                           'vertical-align': 'top', 'border': '1px solid black', 'padding': '20px'}),
                html.Div(
                    children=[
                        html.H2('Key Stats'),
                        html.P(id='text_output', style={
                               'width': '500px', 'text-align': 'center'}),
                    ],
                    style={'width': '700px', 'height': '150px', 'display': 'inline-block'}),

                # Graph 10 avec création de 2 graphiques en fonction du click
                html.Div(
                    children=[
                        html.H2(
                            "Hover a plot to change the minor an major graphs below."),
                        dcc.Graph(id='scatter', figure=ecom_scatter),
                        dcc.Graph(id='major_cat'),
                        dcc.Graph(id='minor_cat'),
                    ]
                ),
                # graph 11 sales volumes vs sales amount by country
                html.Div(
                    children=[
                        html.H3('Sales Volume vs Sales Amount by Country'),
                        html.P(
                            "Click on the scatter and then on the major categories to have the minor."),
                        dcc.Graph(id='scatter', figure=ecom_scatter),
                        dcc.Graph(id='major_cat_2'),
                        dcc.Graph(id='minor_cat_2'),
                    ]
                ),

                # graph12 2 drop down dont un dont les options sont conditionnées par la valeur du premier
                html.Div(
                    children=[
                        html.H2("Sales Breakdown"),
                        html.H3("Major category select : "),
                        dcc.Dropdown(
                            id="major_cat_dd_12",
                            options=[{'label': category, "value": category}
                                     for category in major_categories],
                            style={'width': "200px", "margin": '0 auto'},
                        ),
                        html.H3("Minor category elect: "),
                        dcc.Dropdown(
                            id="minor_cat_dd_12",
                            style={'width': "200px", "margin": '0 auto'},
                        ),
                        dcc.Graph(id=('sales_line_12')),
                    ]
                ),

                # 13 1 dropdown qui conditionne le suivant + 1 titre + une valeur par défaut pour le second drop down

                html.Div(
                    children=[
                        html.H2("Sales Breakdown"),
                        html.H3("Major category select : "),
                        dcc.Dropdown(
                            id="major_cat_dd_13",
                            options=[{'label': category, "value": category}
                                     for category in major_categories],
                            style={'width': "200px", "margin": '0 auto'},
                        ),
                        html.H3("Minor category elect: "),
                        dcc.Dropdown(
                            id="minor_cat_dd_13",
                            style={'width': "200px", "margin": '0 auto'},
                        ),
                        dcc.Graph(id=('sales_line_13')),
                        html.H3(id='chosen_major_cat_title_13')
                    ]
                ),

            ]
        ),
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


# graph 7 ventes par produit

@app.callback(
    Output('search_prod_graph', 'figure'),
    Input('search_prod', 'value')
)
def update_graph_7(search_value):
    title_value = 'None Selected (Showing all)'
    sales = ecom_sales.copy(deep=True)

    if search_value:
        sales = sales[sales['Description'].str.contains(
            search_value, case=False)]
        title_value = search_value

    fig = px.scatter(
        data_frame=sales,
        y='OrderValue',
        x='Quantity',
        color='Country',
        title=f'Sames with description text : {title_value}'
    )
    return fig


# graph 8 ventes en fonction des quantités et des pays avec filtre sur les montants de vente
@app.callback(
    Output("graph8", 'figure'),
    Input("graph8_input_range", "value")
)
def update_graph_8(input_min_value):

    if not input_min_value:
        input_min_value = 0

    sales = ecom_sales.copy(deep=True)

    if input_min_value:
        input_min_value = round(float(input_min_value), 2)
        sales = sales[sales['OrderValue'] > input_min_value]

    fig = px.scatter(
        data_frame=sales,
        x='Quantity',
        y='OrderValue',
        height=400,
        color='Country',
        title=f'Orders of Min Value ${input_min_value}'
    )

    return fig


# graph 9 impression des statistiques
@app.callback(
    Output('text_output', 'children'),
    Input('scatter_fig', 'hoverData'))
def get_key_stats(hoverData):

    if not hoverData:
        return 'Hover over a country to see key stats'

    # Extract the custom data from the hoverData
    country = hoverData['points'][0]['customdata'][0]
    country_df = ecom_sales[ecom_sales['Country'] == country]

    top_major_cat = country_df.groupby('category').agg('size').reset_index(name='Sales Volume').sort_values(
        by='Sales Volume', ascending=False).reset_index(drop=True).loc[0, 'category']
    top_sales_month = country_df.groupby('date')['OrderValue'].agg('sum').reset_index(
        name='Total Sales ($)').sort_values(by='Total Sales ($)', ascending=False).reset_index(drop=True).loc[0, 'date']

    # Use the aggregated variables
    stats_list = [
        f'Key stats for : {country}', html.Br(),
        f'The most popular Major Category by sales volume was: {top_major_cat}', html.Br(
        ),
        f'The highest sales value month was: {top_sales_month.month}/{top_sales_month.year}'
    ]
    return stats_list

# callback 10 : affiche 2 graph mis ) jour en fonction du pays survolé dans le graph scatter.

# Create a callback to update the minor category plot


@app.callback(
    Output('minor_cat', 'figure'),
    Input('scatter', 'hoverData'))
def update_min_cat_hover(hoverData):
    hover_country = 'Australia'

    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    minor_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    minor_cat_agg = minor_cat_df.groupby('Minor Category')['OrderValue'].agg(
        'sum').reset_index(name='Total Sales ($)')
    ecom_bar_minor_cat = px.bar(minor_cat_agg, x='Total Sales ($)', y='Minor Category',
                                orientation='h', height=450, title=f'Sales by Minor Category for: {hover_country}')
    ecom_bar_minor_cat.update_layout(
        {'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'}, 'title': {'x': 0.5}})

    return ecom_bar_minor_cat

# Create a callback to update the major category plot


@app.callback(
    Output('major_cat', 'figure'),
    Input('scatter', 'hoverData'))
def update_major_cat_hover(hoverData):
    hover_country = 'Australia'

    # Conditionally select the country from the hover data
    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    major_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    major_cat_agg = major_cat_df.groupby('Major Category')['OrderValue'].agg(
        'sum').reset_index(name='Total Sales ($)')

    ecom_bar_major_cat = px.bar(major_cat_agg, x='Total Sales ($)',
                                y='Major Category', height=300,
                                title=f'Sales by Major Category for: {hover_country}', color='Major Category',
                                color_discrete_map={'Clothes': 'blue', 'Kitchen': 'red', 'Garden': 'green', 'Household': 'yellow'})
    ecom_bar_major_cat.update_layout(
        {'margin': dict(l=10, r=15, t=40, b=0), 'title': {'x': 0.5}})

    return ecom_bar_major_cat

# callback 11 on hover over graph 1 update graph 2. Then on click on graph 2 update graph 3


@app.callback(
    Output('major_cat_2', 'figure'),
    Input('scatter', 'hoverData'))
def update_major_cat_hover(hoverData):
    hover_country = 'Australia'

    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    major_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    major_cat_agg = major_cat_df.groupby('Major Category')['OrderValue'].agg(
        'sum').reset_index(name='Total Sales ($)')

    ecom_bar_major_cat = px.bar(major_cat_agg, x='Total Sales ($)',
                                # Ensure the Major category will be available
                                custom_data=['Major Category'],
                                y='Major Category', height=300,
                                title=f'Sales by Major Category for: {hover_country}', color='Major Category',
                                color_discrete_map={'Clothes': 'blue', 'Kitchen': 'red', 'Garden': 'green', 'Household': 'yellow'})
    ecom_bar_major_cat.update_layout(
        {'margin': dict(l=10, r=15, t=40, b=0), 'title': {'x': 0.5}})

    return ecom_bar_major_cat

# Set up a callback for click data


@app.callback(
    Output('minor_cat_2', 'figure'),
    Input('major_cat_2', 'clickData'))
def update_major_cat_click(clickData):
    click_cat = 'All'
    major_cat_df = ecom_sales.copy()
    total_sales = major_cat_df.groupby('Country')['OrderValue'].agg(
        'sum').reset_index(name='Total Sales ($)')

    # Extract the major category clicked on for usage
    if clickData:
        click_cat = clickData['points'][0]['customdata'][0]

        # Undetake a filter using the major category clicked on
        major_cat_df = ecom_sales[ecom_sales['Major Category'] == click_cat]

    country_mj_cat_agg = major_cat_df.groupby('Country')['OrderValue'].agg(
        'sum').reset_index(name='Total Sales ($)')
    country_mj_cat_agg['Sales %'] = (
        country_mj_cat_agg['Total Sales ($)'] / total_sales['Total Sales ($)'] * 100).round(1)

    ecom_bar_country_mj_cat = px.bar(country_mj_cat_agg, x='Sales %', y='Country',
                                     orientation='h', height=450, range_x=[0, 100], text='Sales %',
                                     title=f'Global Sales % by Country for Major Category: {click_cat}')
    ecom_bar_country_mj_cat.update_layout(
        {'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'}, 'title': {'x': 0.5}})

    return ecom_bar_country_mj_cat


# Call back 12 : conditional callback with a first drop down which value is conditioning the second drop down
# Create a callback from the Major Category dropdown to the Minor Category Dropdown
@app.callback(
    Output('minor_cat_dd_12', 'options'),
    Input('major_cat_dd_12', 'value'))
def update_minor_dd(major_cat_dd):

    major_minor = ecom_sales[['Major Category',
                              'Minor Category']].drop_duplicates()
    relevant_minor_options = major_minor[major_minor['Major Category']
                                         == major_cat_dd]['Minor Category'].values.tolist()

    # Create and return formatted relevant options with the same label and value
    formatted_relevant_minor_options = [
        {'label': x, 'value': x} for x in relevant_minor_options]
    return formatted_relevant_minor_options

# Create a callback for the Minor Category dropdown to update the line plot


@app.callback(
    Output('sales_line_12', 'figure'),
    Input('minor_cat_dd_12', 'value'))
def update_line(minor_cat):
    minor_cat_title = 'All'
    ecom_line = ecom_sales.copy()

    if minor_cat:
        minor_cat_title = minor_cat
        ecom_line = ecom_line[ecom_line['Minor Category'] == minor_cat]

    ecom_line = ecom_line.groupby(
        ['year'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    line_graph = px.line(ecom_line, x='year',  y='Total Sales ($)',
                         title=f'Total Sales by year for Minor Category: {minor_cat_title}')

    return line_graph


# 13

# One callback to set minor values & HTML output
@app.callback(
    Output('minor_cat_dd_13', 'options'),
    Output('chosen_major_cat_title_13', 'children'),
    Input('major_cat_dd_13', 'value'))
def update_minor_dd(major_cat_dd):

    major_minor = ecom_sales[['Major Category',
                              'Minor Category']].drop_duplicates()
    relevant_minor_options = major_minor[major_minor['Major Category']
                                         == major_cat_dd]['Minor Category'].values.tolist()
    minor_options = [{'label': x, 'value': x} for x in relevant_minor_options]

    if not major_cat_dd:
        major_cat_dd = 'None Selected'
    # Creating string for title
    major_cat_title = f'This is in the Major Category of : {major_cat_dd}'

    # Return the options and title
    return minor_options, major_cat_title

# Create a callback to set a default minor category value


@app.callback(
    Output('minor_cat_dd_13', 'value'),
    Input('minor_cat_dd_13', 'options'))
def select_minor_cat(options):
    chosen_val = 'None'
    if options:
        vals = [x['value'] for x in options]
        chosen_val = random.choice(vals)
    return chosen_val


@app.callback(
    Output('sales_line_13', 'figure'),
    Input('minor_cat_dd_13', 'value'))
def update_line(minor_cat):
    minor_cat_title = 'All'
    ecom_line = ecom_sales.copy()

    if minor_cat:
        minor_cat_title = minor_cat
        ecom_line = ecom_line[ecom_line['Minor Category'] == minor_cat]

    ecom_line = ecom_line.groupby(
        'year')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    line_graph = px.line(ecom_line, x='year',  y='Total Sales ($)',
                         title=f'Total Sales by Month for Minor Category: {minor_cat_title}')

    return line_graph


if __name__ == ('__main__'):
    app.run_server(debug=True)
