import pandas as pd
import sqlite3
import plotly.express as px
import dash
from dash import Dash, html, dcc

# Conexión a la base de datos
conn = sqlite3.connect('database.db')

# Consulta a la base de datos
query = "SELECT * FROM importaciones_pe"
importaciones_peru = pd.read_sql_query(query, conn)

# Preparación de los datos
importacion_peru = pd.melt(importaciones_peru, id_vars=['CONTINENTE', 'PAÍS DE ORIGEN'], var_name='AÑO',
                           value_name='IMPORTACION (millones de US$)')
importacion_peru['IMPORTACION (millones de US$)'] = importacion_peru['IMPORTACION (millones de US$)'] / 1e6
importacion_peru_evol = importacion_peru.groupby('AÑO')['IMPORTACION (millones de US$)'].sum().reset_index()

importacion_pais = importacion_peru.groupby(['CONTINENTE', 'PAÍS DE ORIGEN'])['IMPORTACION (millones de US$)'].sum().reset_index()
importacion_pais = importacion_pais.sort_values('IMPORTACION (millones de US$)', ascending=False)

importacion_pais_top_10 = importacion_pais.head(10)
importaciones_china_eeuu = importacion_peru[importacion_peru['PAÍS DE ORIGEN'].isin(['CHINA', 'ESTADOS UNIDOS'])]

# Cierre de la conexión a la base de datos
conn.close()

# Aplicación Dash para el Gráfico 2
app_graph2 = Dash(__name__)
server_graph2 = app_graph2.server

app_graph2.layout = html.Div([
    dcc.Graph(
        id='graph2',
        figure=px.scatter(
            data_frame=importacion_pais,
            x='CONTINENTE',
            y='IMPORTACION (millones de US$)',
            title='Gráfico 2 - Importaciones por continente de origen (2005-2023)'
        ).update_layout(
            xaxis_title='Continente',
            yaxis_title='Importación (millones de US$)',
            title_font=dict(size=24, family='Arial', color='black'),
            xaxis=dict(title_font=dict(size=18)),
            yaxis=dict(title_font=dict(size=18)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=50, b=50)
        ).add_annotation(
            x='ASIA',
            y=149339,
            text='China',
            showarrow=False,
            font=dict(size=12, color='black'),
            xshift=0,
            yshift=10,
            align='center'
        ).add_annotation(
            x='AMÉRICA',
            y=138991,
            text='Estados Unidos',
            showarrow=False,
            font=dict(size=12, color='black'),
            xshift=0,
            yshift=10,
            align='center'
        )
    )
])

if __name__ == '__main__':
    app_graph2.run_server(debug=True)