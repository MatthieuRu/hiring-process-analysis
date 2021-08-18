import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from src.hiring_process_analysis.db_manager.server import Server
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_conversion_overall
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_conversion_details
from src.hiring_process_analysis.db_manager.get_kpi import get_kpi_offers
from src.hiring_process_analysis.db_manager.get_kpi import get_onsite_question_overview
from src.hiring_process_analysis.db_manager.get_kpi import get_inferviews_table
from src.hiring_process_analysis.db_manager.get_kpi import get_tag_candidate_overview
from src.hiring_process_analysis.app.vizualisation import Vizualisation


# ---------- Parameter of the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
)

app.title = "Hiring-Process"
app_color = {"graph_bg": "#F2F6FC", "graph_line": "#007ACE"}
server = app.server


# ---------- Connext to the database
server = Server(
    ip='0.0.0.0',
    user='application',
    passwd='secretpassword',
    database='application'
) 

vizualisation = Vizualisation(
        get_kpi_conversion_overall(server),
        get_kpi_conversion_details(server),
        get_kpi_offers(server),
        get_onsite_question_overview(server),
        get_tag_candidate_overview(server),
        get_inferviews_table(server)
)


# ---------- Layer of the App

app.layout = html.Div([
    html.Div([
            html.H6("",
                    className="app__header__title"
        )],
        className="app__header__desc",
    ),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                html.H6(
                    "Hiring Process Insights",
                    className="app__header__title",
                    style={'fontSize': 50}
                ),
            ]), width={'size':10}),
        ],  no_gutters=True),
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                html.P(
                    "Displays the main KPIs and important insights of hiring process.",
                    className="app__header__title--grey",
                ),
            ]), width={'size':5}),
        ],  no_gutters=True),
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_conversion_overall_indicator,
                    id="kpi_conversion_overall_indicator"
                    
                ),
            ]), width={'size':3}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_conversion_overall_graph,
                    id="kpi_conversion_overall_graph"
                ),
            ]), width={'size':3}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_conversion_details_graph,
                    id="kpi_conversion_details_graph"
                ),
            ]), width={'size':4}),
        ],  no_gutters=True),
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_offers_junior_indicator,
                    id="kpi_offers_junior_indicator",
                    className="app__header__title--grey",
                ),
            ]), width={'size':3}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_offers_intern_indicator,
                    id="kpi_offers_intern_indicator"
                    
                ),
            ]), width={'size':3}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.kpi_offers_graph,
                    id="kpi_offers_graph"
                ),
            ]), width={'size':4}),
        ],  no_gutters=True),
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.onsite_question_overview_graph,
                    id="onsite_question_overview_graph"
                ),
            ]), width={'size':5}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.interviewers_overview_graph,
                    id="interviewers_overview_graph"
                ),
            ]), width={'size':5}),
        ],  no_gutters=True),
        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size':1}),
            dbc.Col(html.Div([
                dcc.Graph(
                    figure=vizualisation.tag_candidate_overview_graph,
                    id="tag_candidate_overview_graph"
                ),
            ]), width={'size':10}),
        ],  no_gutters=True),
    ])
])


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)