
import pandas as pd
import plotly.express as px
from app import ecom_sales


df = pd.read_csv('data/consultation.csv')

print(df.info())
print(df.shape)
print(df[df['viewerType'] == 'expert'].shape)
