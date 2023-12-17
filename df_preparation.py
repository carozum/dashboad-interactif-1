import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np


# IMPORT DES DONNEES

ecom_sales = pd.read_csv('ecom_sales.csv')

# Add a new column 'year', 'month', 'day' with random values from the years_list
years_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
months_list = range(1, 13)
days_list = range(1, 29)

# add date
ecom_sales['year'] = np.random.choice(years_list, size=len(ecom_sales))
ecom_sales['month'] = np.random.choice(months_list, size=len(ecom_sales))
ecom_sales['day'] = np.random.choice(days_list, size=len(ecom_sales))
ecom_sales['date'] = pd.to_datetime(ecom_sales[['year', 'month', 'day']])

# Add a new column category
categories = ['Household', 'Kitchen', 'Clothes', 'Garden']
ecom_sales['category'] = np.random.choice(categories, size=len(ecom_sales))

# add major and minor categories
majors = ['Household', 'Kitchen', 'Clothes', 'Garden']
minors = ['Tops', 'Shoes', 'Cutlery', 'Turf', 'Hoses', 'Hats', 'Curtains',
          'Lamps', 'Cooking Knives', 'Rugs', 'Chairs', 'Coasters', 'Scales',
          'Plates', 'Seeds', 'Rakes', 'Bowls']
ecom_sales['Major Category'] = np.random.choice(majors, size=len(ecom_sales))
ecom_sales['Minor Category'] = np.random.choice(minors, size=len(ecom_sales))
