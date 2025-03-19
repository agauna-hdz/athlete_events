# -*- coding: utf-8 -*-
"""Actividad6_BI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BJ438NgwzZJSBaTDx_TlWQEjmWUCQFur
"""

#pip install dash plotly pandas

import pandas as pd

url = 'https://raw.githubusercontent.com/agauna-hdz/athlete_events/refs/heads/main/athlete_events.csv '
df = pd.read_csv(url)
df.head()

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Limpiar datos eliminando valores nulos en 'Medal'
df_medals = df.dropna(subset=['Medal'])

# Inicializar la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout del dashboard con pestañas
app.layout = html.Div([
    html.H1("Dashboard de los Juegos Olímpicos", style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="🏠 Resumen General", value="tab1"),
        dcc.Tab(label="🌍 Análisis por País", value="tab2"),
        dcc.Tab(label="🏅 Análisis por Deporte", value="tab3"),
        dcc.Tab(label="📊 Análisis de Atletas", value="tab4"),
    ]),
    html.Div(id="tabs-content")
])

# Callback para cambiar el contenido según la pestaña seleccionada
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_tab_content(tab):
    if tab == "tab1":
        total_atletas = df['ID'].nunique()
        total_ediciones = df['Games'].nunique()
        total_eventos = df['Event'].nunique()

        return html.Div([
            html.H3("Resumen General"),
            html.P(f"Total de atletas: {total_atletas}"),
            html.P(f"Total de ediciones olímpicas: {total_ediciones}"),
            html.P(f"Total de eventos deportivos: {total_eventos}"),
            dcc.Graph(
                figure=px.line(df.groupby('Year').size().reset_index(name='Participación'),
                               x='Year', y='Participación', title="Evolución de la participación")
            )
        ])

    elif tab == "tab2":
        return html.Div([
            html.H3("Análisis por País"),
            dcc.Dropdown(
                id="dropdown_pais",
                options=[{"label": pais, "value": pais} for pais in sorted(df_medals["Team"].dropna().unique())],
                value="United States",
                placeholder="Selecciona un país"
            ),
            dcc.Graph(id="grafico_medallas_pais")
        ])

    elif tab == "tab3":
        return html.Div([
            html.H3("Análisis por Deporte"),
            dcc.Dropdown(
                id="dropdown_deporte",
                options=[{"label": deporte, "value": deporte} for deporte in sorted(df_medals["Sport"].dropna().unique())],
                value="Athletics",
                placeholder="Selecciona un deporte"
            ),
            dcc.Graph(id="grafico_medallas_deporte")
        ])

    elif tab == "tab4":
        return html.Div([
            html.H3("Análisis de Atletas"),
            dcc.Graph(
                figure=px.histogram(df, x='Age', nbins=50, title="Distribución de edades de los atletas")
            ),
            dcc.Graph(
                figure=px.scatter(df, x='Height', y='Weight', color='Sex', title="Altura vs Peso de los atletas")
            )
        ])

# Callback para actualizar el gráfico de medallas por país
@app.callback(
    Output("grafico_medallas_pais", "figure"),
    Input("dropdown_pais", "value")
)
def update_medals_pais(pais):
    df_filtered = df_medals[df_medals['Team'] == pais]
    fig = px.histogram(df_filtered, x='Year', color='Medal', title=f"Medallas ganadas por {pais}")
    return fig

# Callback para actualizar el gráfico de medallas por deporte
@app.callback(
    Output("grafico_medallas_deporte", "figure"),
    Input("dropdown_deporte", "value")
)
def update_medals_deporte(deporte):
    df_filtered = df_medals[df_medals['Sport'] == deporte]
    fig = px.histogram(df_filtered, x='Year', color='Medal', title=f"Medallas en {deporte} a lo largo de la historia")
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)