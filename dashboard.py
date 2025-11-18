import numpy as np
import pandas as pd
from datetime import date
import random
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, dash_table
from IPython.display import HTML
import dash_bootstrap_components as dbc
import import_ipynb
import simulatore





data_inizio = simulatore.data_inizio
data_fine = simulatore.data_fine
mesi_utili = simulatore.mesi_utili





# IMPORTA DATI DAL SIMULATORE

dati = simulatore.simulazione(data_inizio, data_fine, mesi_utili)

df_suolo = dati["df_suolo"]
df_colture = dati["df_colture"]
df_cultivar = dati["df_cultivar"]
df_ettari = dati["df_ettari"]
df_alberi = dati["df_alberi"]
df_alberi_varieta = dati["df_alberi_varieta"]
df_data_utile = dati["df_data_utile"]
df_clima = dati["df_clima"]
df_ciliegeto = dati["df_ciliegeto"]
df_oliveto = dati["df_oliveto"]
df_irrigazione = dati["df_irrigazione"]
df_irrigazione_olive = dati["df_irrigazione_olive"]
df_irrigazione_ciliegie = dati["df_irrigazione_ciliegie"]
df_danni = dati["df_danni"]
df_danni_olive = dati["df_danni_olive"]
df_danni_ciliegie = dati["df_danni_ciliegie"]
df_raccolta = dati["df_raccolta"]
df_raccolta_olive = dati["df_raccolta_olive"]
df_raccolta_ciliegie = dati["df_raccolta_ciliegie"]
df_fertilizzazione = dati["df_fertilizzazione"]
df_fertilizzazione_olive = dati["df_fertilizzazione_olive"]
df_fertilizzazione_ciliegie = dati["df_fertilizzazione_ciliegie"]
df_trattamento = dati["df_trattamento"]
df_trattamento_olive = dati["df_trattamento_olive"]
df_trattamento_ciliegie = dati["df_trattamento_ciliegie"]
df_potatura = dati["df_potatura"]
df_potatura_olive = dati["df_potatura_olive"]
df_potatura_ciliegie = dati["df_potatura_ciliegie"]
df_mansioni = dati["df_mansioni"]
df_costi_totali = dati["df_costi_totali"]
df_costi_melt = dati["df_costi_melt"]













# CALCOLI VARI, UTILITA DA VERIFICARE

df_ricavi = df_raccolta.groupby("Anno")["Ricavo"].sum().reset_index()
df_costi = df_mansioni.groupby("Anno")["Costo_totale_mansione"].sum().reset_index()
df_econ = df_ricavi.merge(df_costi, on="Anno")
df_econ["Margine"] = df_econ["Ricavo"] - df_econ["Costo_totale_mansione"]














# DASH

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


anni_disponibili = sorted(df_clima["Anno"].unique())



app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col(html.H1("      Dashboard - Azienda Agricola Musci", style={"textAlign": "left"}), width=8),
                        dbc.Col("Seleziona Anno", style={"textAlign": "right", "margin": "0 auto"}),
                        dbc.Col([
                                dcc.Dropdown(
                                    id="anno-dropdown",
                                    options=[{"label": str(a), "value": a} for a in anni_disponibili],
                                    value=anni_disponibili[-1],
                                    clearable=False,
                                    style={"width": "100%", "height": "35px", "textAlign": "center", "lineHeight": "100px", "margin": "0 auto"},
                                    className="dropdown-custom"
                                )
                        ]),
                        dbc.Col([
                                dcc.Dropdown(
                                    id="coltura-dropdown",
                                    options=[
                                        {"label": "Tutte", "value": "Tutte"},
                                        {"label": "Oliveto", "value": "Oliveto"},
                                        {"label": "Ciliegeto", "value": "Ciliegeto"}
                                    ],
                                    value="Tutte",
                                    clearable=False,
                                    style={"width": "100%", "height": "35px", "textAlign": "center", "lineHeight": "100px", "margin": "0 auto"},
                                    className="dropdown-custom"
                                )
                        ])
                    ], className="flex-nowrap")
                ]),
                
                dbc.CardBody([

                    
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
#                                dbc.CardHeader(html.B("Resa totale")),
                                dbc.CardBody([
                                    html.H2([html.Span(id="coltura_selezionata"), html.Span(" - "), html.Span(id="anno_selezionato")])
                                ])
                            ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                        ),
                    ], className="flex-nowrap"),

                    
                        dbc.Row([
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Resa totale")),
                                    dbc.CardBody([
                                        html.H3(id="resa_coltura_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Ricavo totale")),
                                    dbc.CardBody([
                                        html.H3(id="ricavo_coltura_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Profitto totale")),
                                    dbc.CardBody([
                                        html.H3(id="profitto_coltura_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Costo totale")),
                                    dbc.CardBody([
                                        html.H3(id="costi_coltura_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Numero irrigazioni")),
                                    dbc.CardBody([
                                        html.H3(id="conta_irrigazioni_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Card([
                                    dbc.CardHeader(html.B("Precipitazioni")),
                                    dbc.CardBody([
                                        html.H3(id="totale_pioggia_annuale")
                                    ])
                                ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3"),
                                width=2
                            ),
                        ], className="flex-nowrap"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("Ettari", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div(id="numero_ettari", style={"textAlign": "center"}),
                                                dcc.Graph(id="grafico-semitorta_ettari", style={"textAlign": "center", "width": "100%", "height": "200px"}, className="flex-nowrap")
                                            ])
                                        ], className="flex-nowrap")
                                    ], style={"backgroundColor": "#5a5a5a"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader([
                                        html.Div("Per ettaro")
                                    ]),
                                    dbc.CardBody([
                                        html.P(id="resa_ettaro_annuale"),
                                        html.P(id="ricavo_ettaro_annuale"),
                                        html.P(id="costi_ettaro_annuale"),
                                        html.P(id="profitto_ettaro_annuale")
                                    ]),
                                ], style={"backgroundColor": "#5a5a5a", "textAlign": "center"}, className="mb-3"),
                                html.Div(id="card_varieta")
                            ], width=2),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("Rese, Costi, Ricavi e Profitti", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-totali", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-ettaro", style={"height": "300px"})),
                                        ], className="flex-nowrap"),
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-albero", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-costi2", style={"height": "300px"}))
                                        ], className="flex-nowrap"),
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-quantita_ciliegeto", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-ricavo_ciliegeto", style={"height": "300px"}))
                                        ], className="flex-nowrap"),
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-varieta", style={"height": "300px"}))
                                        ]),
                                    ], style={"backgroundColor": "#111111"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader("Dati climatici", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-pioggia", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-umidita", style={"height": "300px"}))
                                        ], className="flex-nowrap"),
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-temp_max_min", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-vento", style={"height": "300px"}))
                                        ], className="flex-nowrap")
                                    ], style={"backgroundColor": "#111111"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader("Precipitazioni, umidità del suolo e irrigazioni", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-irrigazione", style={"height": "400px"}))
                                        ], className="flex-nowrap"),
                                    ], style={"backgroundColor": "#111111"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader("NPK e fertilizzazioni", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col(dcc.Graph(id="grafico-fertilizzazione_oliveto", style={"height": "300px"})),
                                            dbc.Col(dcc.Graph(id="grafico-fertilizzazione_ciliegeto", style={"height": "300px"}))
                                        ], className="flex-nowrap"),
                                    ], style={"backgroundColor": "#111111"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader("Stima dei danni", style={"textAlign": "center"}),
                                    dbc.CardBody(dcc.Graph(id="grafico-stima_danni"), style={"backgroundColor": "#111111"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader("Storico", style={"textAlign": "center"}),
                                    dbc.CardBody(dcc.Graph(id="grafico-grafici_riassuntivi"), style={"backgroundColor": "#111111"})
                                ], className="mb-3"),




                                
                            ]),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("Alberi", style={"textAlign": "center"}),
                                    dbc.CardBody([
                                            dbc.Col([
                                                html.Div(id="numero_alberi", style={"textAlign": "center"}),
                                                dcc.Graph(id="grafico-semitorta_alberi", style={"textAlign": "center", "margin": "0 auto"})
                                            ])
                                    ], style={"backgroundColor": "#5a5a5a"})
                                ], className="mb-3"),
                                dbc.Card([
                                    dbc.CardHeader([
                                        html.Div("Per albero"),
                                        html.Div(id="totale_alberi")
                                    ]),
                                    dbc.CardBody([
                                        html.P(id="resa_albero_annuale"),
                                        html.P(id="ricavo_albero_annuale"),
                                        html.P(id="costi_albero_annuale"),
                                        html.P(id="profitto_albero_annuale")
                                    ]),
                                ], style={"backgroundColor": "#5a5a5a", "textAlign": "center"}, className="mb-3"),
                                html.Div(id="card_varieta_albero"),
                            ], width=2)
                        ], className="flex-nowrap"),
                        dbc.Row([
                            dbc.Col([



                                
                                html.Div([
                                    html.H2("Tabella del DataFrame"),
                                    dash_table.DataTable(
                                        id='tabella-df',
                                        columns=[],
                                        data=[],
                                        page_size=400,
                                        style_table={'overflowX': 'auto'},
                                        style_cell={'textAlign': 'left', 'padding': '5px', 'backgroundColor': 'black'},
                                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
                                    )
                                ])



                                        
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([

                            ], width=12),
                        ]),
                    ])
                
            ], className="mb-3")
        ]),
    ], className="flex-nowrap"),
], fluid=True, style={"backgroundColor": "#222", "padding": "10px"})


#style={"minHeight": "100vh", "maxWidth": "100%"},





@app.callback(
    Output("anno_selezionato", "children"),
    Output("coltura_selezionata", "children"),
    Output("grafico-pioggia", "figure"),
    Output("grafico-umidita", "figure"),
    Output("grafico-vento", "figure"),
    Output("grafico-temp_max_min", "figure"),
    Output("grafico-quantita_ciliegeto", "figure"),
    Output("grafico-ricavo_ciliegeto", "figure"),
    Output("grafico-irrigazione", "figure"),
    Output("grafico-fertilizzazione_oliveto", "figure"),
    Output("grafico-fertilizzazione_ciliegeto", "figure"),
    Output("resa_coltura_annuale", "children"),
    Output("ricavo_coltura_annuale", "children"),
    Output("profitto_coltura_annuale", "children"),
    Output("costi_coltura_annuale", "children"),
    Output("conta_irrigazioni_annuale", "children"),
    Output("resa_ettaro_annuale", "children"),
    Output("ricavo_ettaro_annuale", "children"),
    Output("costi_ettaro_annuale", "children"),
    Output("profitto_ettaro_annuale", "children"),
    Output("resa_albero_annuale", "children"),
    Output("ricavo_albero_annuale", "children"),
    Output("costi_albero_annuale", "children"),
    Output("profitto_albero_annuale", "children"),
    Output("card_varieta", "children"),
    Output("totale_pioggia_annuale", "children"),
    Output("card_varieta_albero", "children"),
    Output("grafico-costi2", "figure"),
    Output("grafico-varieta", "figure"),
    Output("grafico-albero", "figure"),
    Output("grafico-totali", "figure"),
    Output("grafico-ettaro", "figure"),
    Output("grafico-semitorta_ettari", "figure"),
    Output("grafico-semitorta_alberi", "figure"),
    Output("grafico-grafici_riassuntivi", "figure"),
    Output("grafico-stima_danni", "figure"),
#    Output('tabella-df', 'columns'),
#    Output('tabella-df', 'data'),
    Input("anno-dropdown", "value"),
    Input("coltura-dropdown", "value")
)





def aggiorna_grafici(anno, coltura):


# TITOLO SCELTA ANNO E COLTURA
    
    anno_selezionato = anno

    if coltura and coltura != "Tutte":
        coltura_selezionata = coltura
    else:
        coltura_selezionata = "Complessivo"


    

        
# GRAFICI CLIMA (8, 9, 10, 11)
    
    df_aggiorna_clima = df_clima[df_clima["Anno"] == anno]

    fig_pioggia = px.line(df_aggiorna_clima, x="Data", y="Precipitazioni_mm", title=f"Precipitazioni {anno}", template="plotly_dark")
    fig_umidita = px.line(df_aggiorna_clima, x="Data", y="Umidità", title=f"Umidità {anno}", template="plotly_dark")
    fig_vento = px.line(df_aggiorna_clima, x="Data", y="Vento", title=f"Vento {anno}", template="plotly_dark")
    fig_temp_max_min = px.line(df_aggiorna_clima, x="Data", y=["Temperatura_MAX", "Temperatura_MIN"], title=f"Andamento Temperature {anno}", template="plotly_dark")



    

# GRAFICI PRODUZIONE E RICAVO PER VARIETA (5, 6)

    df_aggiorna_raccolta = df_raccolta[df_raccolta["Anno"] == anno].copy()
    
    fig_quantita_ciliegeto = px.bar(df_aggiorna_raccolta, x="Anno", y="Quantità", color="Varietà", barmode="group", title=f"Produzione per varietà - {anno}", template="plotly_dark")
    fig_ricavo_ciliegeto = px.bar(df_aggiorna_raccolta, x="Anno", y="Ricavo", color="Varietà", barmode="group", title=f"Ricavo per varietà - {anno}", template="plotly_dark")


    


# CALCOLI PROFITTO - RICAVO HA - QUANTITA HA - PROFITTO HA - RICAVO ALBERI - RICAVO ALBERI - PROFITTO ALBERI
    
    df_aggiorna_coltura = df_aggiorna_raccolta.merge(df_colture, on="Coltura", how="left")
    df_aggiorna_coltura["Ricavo Ha"] = df_aggiorna_coltura["Ricavo"] / df_aggiorna_coltura["Ettari"]
    df_aggiorna_coltura["Ricavo Alberi"] = df_aggiorna_coltura["Ricavo"] / df_aggiorna_coltura["Alberi TOT"]
    df_aggiorna_coltura["Quantità Ha"] = df_aggiorna_coltura["Quantità"] / df_aggiorna_coltura["Ettari"]
    df_aggiorna_coltura["Quantità Alberi"] = df_aggiorna_coltura["Quantità"] / df_aggiorna_coltura["Alberi TOT"]

    df_aggiorna_costi = df_costi_totali[df_costi_totali["Anno"] == anno]
    df_costi = df_aggiorna_costi.groupby("Coltura")["Costo_totale_mansione"].sum().reset_index()
    df_ricavi = df_aggiorna_raccolta.groupby("Coltura")["Ricavo"].sum().reset_index()
    df_profitto = pd.merge(df_ricavi, df_costi, on="Coltura", how="left")
    df_profitto["Profitto"] = df_profitto["Ricavo"] - df_profitto["Costo_totale_mansione"]

    df_aggiorna_profitto = df_colture.merge(df_profitto, on="Coltura", how="left")
    df_aggiorna_profitto["Profitto Ha"] = df_aggiorna_profitto["Profitto"] / df_aggiorna_profitto["Ettari"]
    df_aggiorna_profitto["Profitto Alberi"] = df_aggiorna_profitto["Profitto"] / df_aggiorna_profitto["Alberi TOT"]

    



# GRAFICO IRRIGAZIONE
    
    df_aggiorna_irrigazione_oliveto = df_irrigazione_olive[df_irrigazione_olive["Anno"] == anno]
    df_aggiorna_irrigazione_ciliegeto = df_irrigazione_ciliegie[df_irrigazione_ciliegie["Anno"] == anno]
    df_aggiorna_irrigazione_oliveto = df_aggiorna_irrigazione_oliveto.drop_duplicates(subset=["Data"])
    df_aggiorna_irrigazione_ciliegeto = df_aggiorna_irrigazione_ciliegeto.drop_duplicates(subset=["Data"])

    fig_irrigazione = go.Figure()

    fig_irrigazione.add_trace(go.Bar(
        x=df_aggiorna_clima["Data"],
        y=df_aggiorna_clima["Precipitazioni_mm"],
        name="Pioggia (mm)",
        marker_color="cornflowerblue",
        opacity=0.7
    ))

    df_suolo["Anno"] = pd.to_datetime(df_suolo["Data"]).dt.year
    df_terreno = df_suolo[df_suolo["Anno"] == anno].sort_values("Data")
    df_oliveto = df_terreno[df_terreno["Coltura"] == "Oliveto"]
    df_ciliegeto = df_terreno[df_terreno["Coltura"] == "Ciliegeto"]
    
    fig_irrigazione.add_trace(go.Scatter(
        x=df_oliveto["Data"],
        y=df_oliveto["Umidità suolo (%)"],
        mode="lines+markers",
        name="Umidità suolo Uliveto",
        line=dict(color="lightgreen", width=2)
    ))
    
    fig_irrigazione.add_trace(go.Scatter(
        x=df_ciliegeto["Data"],
        y=df_ciliegeto["Umidità suolo (%)"],
        mode="lines+markers",
        name="Umidità suolo Ciliegeto",
        line=dict(color="deepskyblue", width=2)
    ))

    df_aggiorna_irrigazione_oliveto["Valore Y"] = 5
    fig_irrigazione.add_trace(go.Scatter(
        x=df_aggiorna_irrigazione_oliveto["Data"],
        y=df_aggiorna_irrigazione_oliveto["Valore Y"],
        mode="markers",
        name="Irrigazione Oliveto",
        marker=dict(size=10, color="darkorange", symbol="circle")
    ))

    df_aggiorna_irrigazione_ciliegeto["Valore Y"] = 35
    fig_irrigazione.add_trace(go.Scatter(
        x=df_aggiorna_irrigazione_ciliegeto["Data"],
        y=df_aggiorna_irrigazione_ciliegeto["Valore Y"],
        mode="markers",
        name="Irrigazione Ciliegeto",
        marker=dict(size=10, color="red", symbol="circle")
    ))

    fig_irrigazione.update_layout(
        title=f"Andamento pioggia e irrigazioni - {anno}",
        template="plotly_dark",
        height=400,
    )



    

# GRAFICO FERTILIZZAZIONE & SUOLO PER OLIVETO
    
    df_suolo["Anno"] = pd.to_datetime(df_suolo["Data"]).dt.year
    df_terreno = df_suolo[df_suolo["Anno"] == anno].sort_values("Data")
    
    df_oliveto = df_terreno[df_terreno["Coltura"] == "Oliveto"]
    df_ciliegeto = df_terreno[df_terreno["Coltura"] == "Ciliegeto"]


    df_fertilizzazione_oliveto = df_fertilizzazione_olive[df_fertilizzazione_olive["Anno"] == anno]
    df_fertilizzazione_oliveto = df_fertilizzazione_oliveto.drop_duplicates(subset=["Data"])
    df_fertilizzazione_oliveto["Valore Y"] = 100
    
    fig_fertilizzazione_oliveto = px.line(
        df_oliveto,
        x="Data",
        y=["Azoto N (%)","Fosforo P (mg/kg)","Potassio K (mg/kg)"],
        title=f"Andamento NPK e fertilizzazioni oliveto - {anno}",
        markers=True,
        template="plotly_dark",
        height=300,
        labels={'variable': ''}
    )
    fig_fertilizzazione_oliveto.add_trace(go.Scatter(
        x=df_fertilizzazione_oliveto["Data"],
        y=df_fertilizzazione_oliveto["Valore Y"],
        mode="markers",
        name="Fertilizzazione",
        marker=dict(size=10, color="darkorange", symbol="star")
    ))
    fig_fertilizzazione_oliveto.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )


    


# GRAFICO FERTILIZZAZIONE & SUOLO PER CILIEGETO

    df_fertilizzazione_ciliegeto = df_fertilizzazione_ciliegie[df_fertilizzazione_ciliegie["Anno"] == anno]
    df_fertilizzazione_ciliegeto = df_fertilizzazione_ciliegeto.drop_duplicates(subset=["Data"])
    df_fertilizzazione_ciliegeto["Valore Y"] = 100
    
    fig_fertilizzazione_ciliegeto = px.line(
        df_ciliegeto,
        x="Data",
        y=["Azoto N (%)","Fosforo P (mg/kg)","Potassio K (mg/kg)"],
        title=f"Andamento NPK e fertilizzazioni ciliegeto - {anno}",
        markers=True,
        template="plotly_dark",
        height=300,
        labels={'variable': ''}
    )
    fig_fertilizzazione_ciliegeto.add_trace(go.Scatter(
        x=df_fertilizzazione_ciliegeto["Data"],
        y=df_fertilizzazione_ciliegeto["Valore Y"],
        mode="markers",
        name="Fertilizzazione",
        marker=dict(size=10, color="darkorange", symbol="star")
    ))
    fig_fertilizzazione_ciliegeto.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )




    







# GRAFICO DANNI

    df_danni_melt = df_danni.melt(id_vars=["Anno", "Coltura"], var_name="Tipo Danno", value_name="Intensità (%)")
    stima_danni = px.line(
        df_danni_melt,
        x="Anno",
        y="Intensità (%)",
        color="Tipo Danno",
        line_group="Tipo Danno",
        facet_col="Coltura",
        markers=True,
        template="plotly_dark",
        height=300
    )





# GRAFICO RIASSUNTIVO (RICAVO E PRODUZIONE)

    torta_ricavi_totali = px.sunburst(df_raccolta, path=["Anno", "Coltura", "Varietà"], values='Ricavo')
    torta_quantità_totali = px.sunburst(df_raccolta, path=["Anno", "Coltura", "Varietà"], values='Quantità')

    grafici_riassuntivi = make_subplots(rows=1, cols=2, subplot_titles=("Ricavi", "Produzione"), specs=[[{"type": "domain"}, {"type": "domain"}]])
    grafici_riassuntivi.add_trace(torta_ricavi_totali.data[0], row=1, col=1)
    grafici_riassuntivi.add_trace(torta_quantità_totali.data[0], row=1, col=2)
    grafici_riassuntivi.update_layout(font_color="#ffffff", paper_bgcolor="#111111", height=300, margin=dict(l=00, r=00, t=30, b=00))










# CALCOLO CARDS

    
    if coltura and coltura != "Tutte":
        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Coltura"] == coltura]
    
    df_raccolta_filtrato = df_aggiorna_raccolta.copy()
    
    resa_coltura_somma = df_raccolta_filtrato["Quantità"].sum()
    resa_coltura_annuale = html.Div([f"{resa_coltura_somma:,d} kg"])

    ricavo_coltura_somma = df_raccolta_filtrato["Ricavo"].sum()
    ricavo_coltura_annuale = html.Div([f"{ricavo_coltura_somma:,.2f} €",])
    

    if coltura and coltura != "Tutte":
        profitto_coltura_somma = df_profitto[df_profitto["Coltura"] == coltura]["Profitto"].sum()
        costi_coltura_somma = df_aggiorna_costi[df_aggiorna_costi["Coltura"] == coltura]["Costo_totale_mansione"].sum()
        irrigazioni_filtrato = df_irrigazione[(df_irrigazione["Anno"] == anno) & (df_irrigazione["Coltura"] == coltura)]
    else:
        profitto_coltura_somma = df_profitto["Profitto"].sum()
        costi_coltura_somma = df_aggiorna_costi["Costo_totale_mansione"].sum()
        irrigazioni_filtrato = df_irrigazione[df_irrigazione["Anno"] == anno]

    profitto_coltura_annuale = html.Div([f"{profitto_coltura_somma:,.2f} €"])
    costi_coltura_annuale = html.Div([f"{costi_coltura_somma:,.2f} €"])
    conta_irrigazioni = len(irrigazioni_filtrato)
    conta_irrigazioni_annuale = html.Div([f"{conta_irrigazioni:,d}"])







    df_aggiorna_alberi_ettari = df_aggiorna_coltura.drop_duplicates(subset=["Coltura"])
    
    totale_resa = df_aggiorna_coltura["Quantità"].sum()
    totale_ricavo = df_aggiorna_coltura["Ricavo"].sum()
    totale_ettari = df_aggiorna_alberi_ettari["Ettari"].sum()
    totale_alberi = df_aggiorna_alberi_ettari["Alberi TOT"].sum()
    
    
    if coltura and coltura != "Tutte":
        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Coltura"] == coltura]
        df_aggiorna_coltura = df_aggiorna_coltura[df_aggiorna_coltura["Coltura"] == coltura]
        df_aggiorna_profitto = df_aggiorna_profitto[df_aggiorna_profitto["Coltura"] == coltura]

        
    
        resa_ettaro = df_aggiorna_coltura["Quantità Ha"].sum()
        ricavo_ettaro = df_aggiorna_coltura["Ricavo Ha"].sum()
        df_aggiorna_profitto["Costi Ha"] = df_aggiorna_profitto["Costo_totale_mansione"] / df_aggiorna_profitto["Ettari"]
        costi_ettaro = df_aggiorna_profitto["Costi Ha"].sum()
        profitto_ettaro = df_aggiorna_profitto["Profitto Ha"].sum()


        resa_albero = df_aggiorna_coltura["Quantità Alberi"].sum()
        ricavo_albero = df_aggiorna_coltura["Ricavo Alberi"].sum()
        df_aggiorna_profitto["Costi Alberi"] = df_aggiorna_profitto["Costo_totale_mansione"] / df_aggiorna_profitto["Alberi TOT"]
        costi_albero = df_aggiorna_profitto["Costi Alberi"].sum()
        profitto_albero = df_aggiorna_profitto["Profitto Alberi"].sum()
        


    else:
        resa_ettaro = totale_resa / totale_ettari
        ricavo_ettaro = totale_ricavo / totale_ettari
        costi_ettaro = df_aggiorna_profitto["Costo_totale_mansione"].sum() / totale_ettari
        profitto_ettaro = df_aggiorna_profitto["Profitto"].sum() / totale_ettari
        

        resa_albero = totale_resa / totale_alberi
        ricavo_albero = totale_ricavo / totale_alberi
        costi_albero = df_aggiorna_profitto["Costo_totale_mansione"].sum() / totale_alberi
        profitto_albero = df_aggiorna_profitto["Profitto"].sum() / totale_alberi


        
    resa_ettaro_annuale = html.Div(["RESA", html.Br(), f"{resa_ettaro:,.2f} kg", html.Br(), html.Br()])
    ricavo_ettaro_annuale = html.Div(["RICAVO", html.Br(), f"{ricavo_ettaro:,.2f} kg", html.Br(), html.Br()])
    costi_ettaro_annuale = html.Div(["COSTI", html.Br(), f"{costi_ettaro:,.2f} kg", html.Br(), html.Br()])
    profitto_ettaro_annuale = html.Div(["PROFITTO", html.Br(), f"{profitto_ettaro:,.2f} kg", html.Br(), html.Br()])
    
    resa_albero_annuale = html.Div(["RESA", html.Br(), f"{resa_albero:,.2f} kg", html.Br(), html.Br()])
    ricavo_albero_annuale = html.Div(["RICAVO", html.Br(), f"{ricavo_albero:,.2f} €", html.Br(), html.Br()])
    costi_albero_annuale = html.Div(["COSTI", html.Br(), f"{costi_albero:,.2f} €", html.Br(), html.Br()])
    profitto_albero_annuale = html.Div(["PROFITTO", html.Br(), f"{profitto_albero:,.2f} €", html.Br(), html.Br()])



    
    if coltura and coltura != "Tutte":
        df_colture_filtrato = df_colture[df_colture["Coltura"] == coltura]
        numero_ettari = df_colture_filtrato["Ettari"].sum()
        numero_alberi = df_colture_filtrato["Alberi TOT"].sum()
    else:
        numero_ettari = totale_ettari
        numero_alberi = totale_alberi

    

    df_varieta = df_raccolta_filtrato.groupby("Varietà")[["Quantità","Ricavo"]].sum().reset_index()
    df_varieta["Prezzo medio"] = df_varieta["Ricavo"] / df_varieta["Quantità"]
    
    card_varieta = [
        dbc.Card(
            [
            dbc.CardHeader(row["Varietà"] + " (totale)"),
            dbc.CardBody([
                html.P(["RESA", html.Br(), f"{row['Quantità']:,.2f} kg"]),
                html.P(["RICAVO", html.Br(), f"{row['Ricavo']:,.2f} €"]),
                html.P(["PREZZO MEDIO (Kg)", html.Br(), f"{row['Prezzo medio']:,.2f} €"])
            ])
        ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3")
    for _, row in df_varieta.iterrows()
    ]

    df_varieta = df_raccolta_filtrato.groupby("Varietà")[["Quantità", "Ricavo"]].sum().reset_index()
    df_varieta = pd.merge(df_varieta, df_alberi_varieta, on="Varietà", how="left")

    df_varieta["Quantità Albero"] = df_varieta["Quantità"] / df_varieta["Alberi"]
    df_varieta["Ricavo Albero"] = df_varieta["Ricavo"] / df_varieta["Alberi"]

    media_resa_albero = df_varieta["Quantità Albero"].mean()
    df_varieta["IPR"] = df_varieta["Quantità Albero"] / media_resa_albero

    
    card_varieta_albero = [
        dbc.Card(
            [
            dbc.CardHeader(row["Varietà"] + " (per albero)"),
            dbc.CardBody([
                html.P(["RESA", html.Br(), f"{row['Quantità Albero']:,.2f} kg"]),
                html.P(["RICAVO", html.Br(), f"{row['Ricavo Albero']:,.2f} €"]),
                html.P(["IPR", html.Br(), f"{row['IPR']:,.2f} €"])
            ])
        ], color="#5a5a5a", style={"textAlign": "center"}, className="mb-3")
    for _, row in df_varieta.iterrows()
    ]


 
    totale_pioggia_anno = df_aggiorna_clima["Precipitazioni_mm"].sum()
    totale_pioggia_annuale = html.Div([f"{totale_pioggia_anno:,.0f} mm"])



    
    df_aggiorna_raccolta = df_raccolta.merge(df_profitto[["Coltura","Profitto"]], on="Coltura", how="left")
    df_aggiorna_raccolta = df_aggiorna_raccolta.merge(df_colture[["Coltura","Ettari","Alberi TOT"]], on="Coltura", how="left")

    df_aggiorna_raccolta["Profitto Ha"] = df_aggiorna_raccolta["Profitto"] / df_aggiorna_raccolta["Ettari"]
    df_aggiorna_raccolta["Profitto Alberi"] = df_aggiorna_raccolta["Profitto"] / df_aggiorna_raccolta["Alberi TOT"]
    
    df_varieta_merge = df_varieta.merge(df_aggiorna_raccolta[["Varietà", "Profitto Alberi"]], on=["Varietà"], how="left")


    fig_costi2 = px.bar(
        df_aggiorna_costi,
        x="Costo_totale_mansione",
        y="Attività",
        color="Coltura",
        orientation="h",
        barmode="stack",
        title=f"Costi specifici per attività - {anno}",
        template="plotly_dark"
    )
    fig_costi2.update_layout(yaxis={'categoryorder':'total ascending'})
    

    fig_varieta = px.treemap(
        df_aggiorna_coltura,
        path=["Coltura","Varietà"],
        values="Quantità",
        color="Ricavo",
        color_continuous_scale="Viridis",
        title=f"Produzione e Ricavo per Varietà - {anno}",
        template="plotly_dark"
    )


    fig_albero = px.scatter(
        df_varieta_merge,
        x="Quantità Albero",
        y="Ricavo Albero",
        size="Profitto Alberi",
        color="Varietà",
        hover_data=["IPR"],
        title=f"Produzione e Ricavo per albero - {anno}",
        template="plotly_dark"
    )
    fig_albero.update_layout(
        xaxis_title="Produzione per albero (kg)",
        yaxis_title="Ricavo per albero (€)"
    )











    
    df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Anno"] == anno]
    
    if coltura and coltura != "Tutte":
        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Coltura"] == coltura]

# agg in quanto quantita e ricavo sono la somma di dati parziali, profitto è già totale
    df_totali = df_aggiorna_raccolta.groupby(["Anno", "Coltura"], as_index=False).agg({"Quantità": "sum", "Ricavo": "sum", "Profitto": "first"})
    df_totali = df_totali.merge(df_costi, on="Coltura", how="left")
    
    df_raccolta_melt = df_totali.melt(
        id_vars=["Anno", "Coltura"],
        value_vars=["Quantità","Ricavo","Costo_totale_mansione","Profitto"],
        var_name="Prova",
        value_name="Valore"
    )

    fig_totali = px.bar(
        df_raccolta_melt,
        x="Anno",
        y="Valore",
        color="Coltura",
        barmode="stack",
        facet_col="Prova",
        title=f"Produzione, Ricavo, Costi e Profitto Totali - {anno}",
        template="plotly_dark"
    )
    fig_totali.update_xaxes(title_text="")




# aggrega df per evitare somma di totali in ricavo e in resa in oliveto
    
    
    df_coltura_agg = df_aggiorna_coltura.groupby(["Anno", "Coltura", "Varietà"], as_index=False).agg({"Quantità Ha": "sum", "Ricavo Ha": "sum"})

    df_raccolta_agg = df_aggiorna_raccolta.groupby(["Anno", "Coltura", "Varietà"], as_index=False).agg({"Profitto Ha": "first"})

    df_ettaro = df_raccolta_agg.merge(df_coltura_agg, on=["Anno", "Coltura", "Varietà"], how="left")

    df_ettaro = df_ettaro.groupby(["Anno", "Coltura"], as_index=False).agg({"Quantità Ha": "sum", "Ricavo Ha": "sum", "Profitto Ha": "first"})


    df_costi_ettaro = df_aggiorna_profitto.copy()
    df_costi_ettaro["Costi Ha"] = df_costi_ettaro["Costo_totale_mansione"] / df_costi_ettaro["Ettari"]
    df_ettaro = df_ettaro.merge(df_costi_ettaro[["Coltura", "Costi Ha"]], on="Coltura", how="left")


    fig_ettaro = px.bar(
        df_ettaro,
        x="Coltura",
        y=["Quantità Ha", "Ricavo Ha", "Costi Ha", "Profitto Ha"],
        barmode="group",
        title=f"Produzione, Ricavo e Profitto per Ettaro - {anno}",
        template="plotly_dark"
    )
    fig_ettaro.update_layout(
        yaxis_title="kg / €",
    )


    

    
# GRAFICO SEMITORTA ETTARI

    fig_semitorta_ettari = go.Figure(go.Indicator(
        mode="gauge+number",
        value=numero_ettari,
        gauge={'axis': {'range': [0, totale_ettari]}, 'bar': {'color': 'green', 'thickness': 0.6}},
        domain={'x': [0.1, 0.9], 'y': [0, 1]}
    ))
    fig_semitorta_ettari.update_layout(
        height=200,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="#5a5a5a",
        plot_bgcolor="#5a5a5a",
        font_color="#ffffff"
    )




    
# GRAFICO SEMITORTA ALBERI
    
    fig_semitorta_alberi = go.Figure(go.Indicator(
        mode="gauge+number",
        value=numero_alberi,
        gauge={'axis': {'range': [0, totale_alberi]}, 'bar': {'color': 'blue', 'thickness': 0.6}},
        domain={'x': [0.1, 0.9], 'y': [0, 1]} 
    ))
    fig_semitorta_alberi.update_layout(
        height=200,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="#5a5a5a",
        plot_bgcolor="#5a5a5a",
        font_color="#ffffff"
    )

    






    
# GRAFICO PRODUZIONE PER VARIETA

    if coltura and coltura != "Tutte":
        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Coltura"] == coltura]

        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Anno"] == anno].copy()
        fig_quantita_ciliegeto = px.bar(
            df_aggiorna_raccolta.groupby(["Anno", "Varietà"])["Quantità"].sum().reset_index(),
            x="Anno",
            y="Quantità",
            color="Varietà",
            barmode="group",
            title="Produzione per anno e coltura",
            template="plotly_dark",
            text_auto=".2s"
        )

        
        
# GRAFICO RICAVO PER VARIETA
        
        df_aggiorna_raccolta = df_aggiorna_raccolta[df_aggiorna_raccolta["Anno"] == anno].copy()
        fig_ricavo_ciliegeto = px.bar(
            df_aggiorna_raccolta.groupby(["Anno", "Varietà"])["Ricavo"].sum().reset_index(),
            x="Anno",
            y="Ricavo",
            color="Varietà",
            barmode="group",
            title="Ricavo per anno e varietà",
            template="plotly_dark",
            text_auto=".2s"
        )





# per la visualizz del df, da cancellare alla fine

    
    df_ciliegeto = df_ciliegeto[df_ciliegeto["Anno"] == anno]
    if coltura != "Tutte":
        
        df_ciliegeto = df_ciliegeto[df_ciliegeto["Coltura"] == coltura]
#    else:
    columns=[{"name": i, "id": i} for i in df_ciliegeto.columns]
    data=df_ciliegeto.to_dict('records')








    
    
    
    for fig in [fig_pioggia, fig_umidita, fig_vento, fig_temp_max_min, fig_quantita_ciliegeto, fig_ricavo_ciliegeto, fig_fertilizzazione_oliveto, fig_fertilizzazione_ciliegeto, fig_costi2, fig_varieta, fig_albero, fig_totali, fig_ettaro]:
        fig.update_traces(marker_line_width=0, opacity=0.99)
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            margin=dict(l=40, r=40, t=70, b=40)
        )

    return anno_selezionato, coltura_selezionata, fig_pioggia, fig_umidita, fig_vento, fig_temp_max_min, fig_quantita_ciliegeto, fig_ricavo_ciliegeto, fig_irrigazione, fig_fertilizzazione_oliveto, fig_fertilizzazione_ciliegeto, resa_coltura_annuale, ricavo_coltura_annuale, profitto_coltura_annuale, costi_coltura_annuale, conta_irrigazioni_annuale, resa_ettaro_annuale, ricavo_ettaro_annuale, costi_ettaro_annuale, profitto_ettaro_annuale, resa_albero_annuale, ricavo_albero_annuale, costi_albero_annuale, profitto_albero_annuale, card_varieta, totale_pioggia_annuale, card_varieta_albero, fig_costi2, fig_varieta, fig_albero, fig_totali, fig_ettaro, fig_semitorta_ettari, fig_semitorta_alberi, grafici_riassuntivi, stima_danni












if __name__ == "__main__":
    app.run(debug=True, port=8050, mode="inline")
