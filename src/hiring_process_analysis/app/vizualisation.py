
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class Vizualisation:
    """A Vizualisation Class."""

    def __init__(
        self,
        kpi_conversion_overall: pd.DataFrame,
        kpi_conversion_details: pd.DataFrame,
        kpi_offers: pd.DataFrame,
        onsite_question_overview: pd.DataFrame,
        tag_candidate_overview: pd.DataFrame,
        interviews: pd.DataFrame
    ) -> None:
        self.app_color = {"graph_bg": "#F2F6FC", "graph_line": "#007ACE"}

        # conversion Overall
        self.kpi_conversion_overall = kpi_conversion_overall
        self.kpi_conversion_details = kpi_conversion_details

        self.kpi_conversion_overall_graph = self._get_kpi_conversion_overall_graph()
        self.kpi_conversion_overall_indicator = self._get_kpi_conversion_overall_indicator()

        # conversion details
        self.kpi_conversion_details_graph = self._get_kpi_conversion_details_graph()

        # KPI offers Accepted
        self.kpi_offers = kpi_offers
        self.kpi_offers_graph = self._get_kpi_offers_graph()
        self.kpi_offers_intern_indicator = self._get_kpi_offers_intern_indicator()
        self.kpi_offers_junior_indicator = self._get_kpi_offers_junior_indicator()

        # Onsite Question Overview
        self.onsite_question_overview = onsite_question_overview
        self.onsite_question_overview_graph = self._get_onsite_question_overview_graph()

        # Tag Candidate Overview
        self.tag_candidate_overview = tag_candidate_overview
        self.tag_candidate_overview_graph = self._get_tag_candidate_overview_graph()

        # Interviewer Overview
        self.interviews = interviews
        self.interviewers_overview_graph = self._get_interviewer_overview_graph()


    def _get_kpi_conversion_overall_graph(self):

        fig = px.bar(
            self.kpi_conversion_overall,
            x='Funnel',
            y='Number of Candidates',
            title = "Overall Conversion",
            labels={
                    "Funnel": ""
                }
        )
        fig.update_layout(yaxis={'visible': False})
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])

        return fig

    def _get_kpi_conversion_overall_indicator(self):
        indicator_conversion = self.kpi_conversion_details.at[
            3,
            'Number of Candidates' 
        ]  / self.kpi_conversion_details.at[
            0,
            'Number of Candidates' 
        ] * 100

        indicator_offers = self.kpi_conversion_details.at[
            4,
            'Number of Candidates' 
        ]  / self.kpi_conversion_details.at[
            3,
            'Number of Candidates' 
        ] * 100

        fig = make_subplots(
            rows=2,
            cols=1,
            specs=[[{"type": "domain"}],
           [{"type": "domain"}]],
        )

        fig.add_trace(go.Indicator(
            value = indicator_conversion,
            domain = {'row': 0, 'column': 1},
            title = "Interview to offer conversion: (%)",
        ), row=1, col=1
        )
        fig.add_trace(go.Indicator(
            value = indicator_offers,
            domain = {'row': 0, 'column': 1},
            title = "Offers accepted conversion (%)",
        ), row=2, col=1
        )
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(font = dict(size=18))
        return fig

    def _get_kpi_conversion_details_graph(self):

        fig = px.bar(
            self.kpi_conversion_details,
            x='Funnel',
            y='Number of Candidates',
            title = "Candidate overview by each process",
            labels={
                "Funnel": ""
            }
        )
        
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])

        return fig


    def _get_kpi_offers_intern_indicator(self):
        indicator = self.kpi_offers.at[
            0,
            'Accepted Offers' 
        ]  / self.kpi_offers.at[
            0,
            'Offers' 
        ] * 100

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            value = indicator,
            domain = {'row': 0, 'column': 1},
            title = "Offer acceptation rate for New Grad Position (%)"
        ))
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

    def _get_kpi_offers_junior_indicator(self):
        indicator = self.kpi_offers.at[
            1,
            'Accepted Offers' 
        ]  / self.kpi_offers.at[
            1,
            'Offers' 
        ] * 100

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            value = indicator,
            domain = {'row': 0, 'column': 1},
            title = "Offer acceptation rate for Intern Position (%)"
        ))
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

    def _get_kpi_offers_graph(self):
        self.kpi_offers['Rejected Offers'] = self.kpi_offers['Offers'] - \
            self.kpi_offers["Accepted Offers"]

        fig = px.bar(
            self.kpi_offers,
            x="Job name",
            y=[
                "Rejected Offers",
                "Accepted Offers"
            ],
            title="Offers Overview per Job",
            labels={
                "value": "Number of Candidates",
                "variable": "Legend",
                "Job name": ""

            }
        )
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

    def _get_onsite_question_overview_graph(self):
        self.onsite_question_overview['Onsite Question'] = self.onsite_question_overview[
            'Onsite Question'
        ].str.replace('Onsite Value Fit ', '')
        fig = px.bar(
            self.onsite_question_overview,
            x="Onsite Question",
            y="% of Candidate Not Hired",
            title="Feedback by Onsite Value Fit",
            labels={
                "variable": "Legend",
                "Onsite Question": ""

            }
        )
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

    
    def _get_tag_candidate_overview_graph(self):
        self.tag_candidate_overview = self.tag_candidate_overview[
            (self.tag_candidate_overview['Candidate Rejected the offer'] > 0) |
            (self.tag_candidate_overview['Candidate Accepted the offer'] > 0)
        ]

        fig = px.bar(
            self.tag_candidate_overview,
            x="tag",
            y=[
                'Candidate Rejected the offer',
                'Candidate Accepted the offer'
            ],
            title="Acceptance Ratio per Tag",
            labels={
                "variable": "Legend",
                "tag": "",
                "value": "Number of Candidates",
            }
        )
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

    def _get_interviewer_overview_graph(self):
        self.interviews['Feedback'] = self.interviews['score'].map(
            {
                '1 - Strong No Hire': 'Negative',
                '2 - No Hire': 'Negative',
                '3 - Hire': 'Positive',
                '4 - Strong Hire': 'Positive',
            }
        )
        interviewers = self.interviews.groupby(
            ['interviewer_id', 'Feedback']
        ).size().reset_index().rename(
            columns={0: 'Number of Interviews'}
        )

        fig = px.bar(
            interviewers,
            x='interviewer_id',
            y='Number of Interviews',
            title="Feedback per Interviewers",
            color='Feedback',
            labels={
                "interviewer_id": "Interviewer",
            }
        )
        fig.update_xaxes(showticklabels=False)
        fig.update_layout(plot_bgcolor = self.app_color["graph_bg"])
        fig.update_layout(paper_bgcolor = self.app_color["graph_bg"])
        return fig

