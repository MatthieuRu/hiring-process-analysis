import pandas as pd
from .server import Server

class Migration():

    def __init__(
        self,
        interview: pd.DataFrame,
        candidate_tags: pd.DataFrame,
        offer_accepts: pd.DataFrame,
        offers: pd.DataFrame,
    ) -> None:
        """[summary]

        Args:
            candidate_tags (pd.DataFrame): [description]
            interview (pd.DataFrame): [description]
            offer_accepts (pd.DataFrame): [description]
            offers (pd.DataFrame): [description]
        """
        
        self.candidates = pd.concat([
            candidate_tags[['CANDIDATE_ID']],
            interview[['CANDIDATE_ID']],
            offers[['CANDIDATE_ID']]
        ]).drop_duplicates('CANDIDATE_ID')
        self.candidates.columns= self.candidates.columns.str.lower()

        self.candidate_tags = candidate_tags.drop_duplicates()
        self.candidate_tags.columns= self.candidate_tags.columns.str.lower()

        self.interview = interview.drop_duplicates(
            ['CANDIDATE_ID', 'INTERVIEW_NAME','JOB_POSTING_NAME', 'INTERVIEWER_ID', 'SCORE']
        )
        self.interview.columns= self.interview.columns.str.lower()

        self.offer_accepts = offer_accepts
        self.offer_accepts.columns= self.offer_accepts.columns.str.lower()

        self.offers = offers
        self.offers.columns= self.offers.columns.str.lower()


    def send_to_databases(self, server: Server) -> 1:

        server.db['hiring_process'].tb['candidates'].append_dataframe(
            self.candidates
        )
        server.db['hiring_process'].tb['interviews'].append_dataframe(
            self.interview
        )
        server.db['hiring_process'].tb['candidate_tags'].append_dataframe(
            self.candidate_tags
        )
        server.db['hiring_process'].tb['offers'].append_dataframe(
            self.offers
        )
        server.db['hiring_process'].tb['offer_accepts'].append_dataframe(
            self.offer_accepts
        )
        return 1