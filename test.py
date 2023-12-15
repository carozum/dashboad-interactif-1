
import pandas as pd
import plotly.express as px
from app import ecom_sales

df = ecom_sales.copy(deep=True)
print(df['date'].loc[0].strftime('%d/%m/%Y')
      )


fig = px.bar()
fig.show()
