import pandas as pd
from .server import Server


def get_kpi_offers(server: Server) -> pd.DataFrame:
    query = """
        --- Look if we hire the people we want
        select 
            oa.job_posting_name as "Job name",
            "Offers",
            "Accepted Offers"
        from (
            select 
                job_posting_name,
                count(*) as "Offers"
            from hiring_process.offers 
            group by job_posting_name
        ) as o
        inner join (
            select 
                job_posting_name,
                count(*) as "Accepted Offers"
            from hiring_process.offer_accepts 
            group by job_posting_name
        )  oa
        on oa.job_posting_name = o.job_posting_name;
    """
    return server._execute_extract(query)


def get_kpi_conversion_overall(server: Server) -> pd.DataFrame:
    query = """
        select
            'Total of Candidates' AS "Funnel",
            COUNT( distinct i.candidate_id) AS "Number of Candidates"
        FROM hiring_process.interviews as i
        union all
        select
                'Accepted Offers' AS "Funnel",
            COUNT( distinct oa.candidate_id) AS "Number of Candidates"
        FROM hiring_process.offer_accepts as oa;
    """
    return server._execute_extract(query)


def get_kpi_conversion_details(server: Server) -> pd.DataFrame:
    query = """
        select
                'Interview Phone Screen #1' AS "Funnel",
            COUNT( distinct i.candidate_id) AS "Number of Candidates"
        FROM hiring_process.interviews as i
        where interview_name in ('Phone Screen #1') 
        union all
        select
                'Interview Phone Screen #2' AS "Funnel",
            COUNT( distinct i.candidate_id) AS "Number of Candidates"
        FROM hiring_process.interviews as i
        where interview_name in ('Phone Screen #2') 
        union all
        select
                'Interview Onsite' AS "Funnel",
            COUNT( distinct i.candidate_id) AS "Number of Candidates"
        FROM hiring_process.interviews as i
        where interview_name like '%Onsite%' 
        union all
        select
                'Offer Process' AS "Funnel",
            COUNT( distinct o.candidate_id) AS "Number of Candidates"
        FROM hiring_process.offers as o
        union all
        select
                'Accepted Offers' AS "Funnel",
            COUNT( distinct oa.candidate_id) AS "Number of Candidates"
        FROM hiring_process.offer_accepts as oa;
    """
    return server._execute_extract(query)


def get_onsite_question_overview(server: Server) -> pd.DataFrame:
    query = """
        select
            onsite_fit_question.interview_name as "Onsite Question",
            onsite_fit_question.number_candidate_fit_question as "Number of Candidate",
            onsite_fit_question_not_hire.number_candidate_fit_question_not_hire as "Not Hire Candidate",
            -- Get number in percentage
            onsite_fit_question_not_hire.number_candidate_fit_question_not_hire::NUMERIC  / onsite_fit_question.number_candidate_fit_question *100
            as "% of Candidate Not Hired"
        from (
            -- number of time we asked the different question
            select interview_name ,
            count(*) as number_candidate_fit_question 
            from hiring_process.interviews
            where interview_name in (
                'Onsite Value Fit Question - A',
                'Onsite Value Fit Question - B',
                'Onsite Value Fit Question - C',
                'Onsite Value Fit Question - D'
            )
            group by interview_name
        ) as onsite_fit_question
        inner join (
            -- number of time we asked the different question and we not hire the candidates
            select interview_name, 
            count(*)  as number_candidate_fit_question_not_hire 
            from hiring_process.interviews 
            where interview_name in (
                'Onsite Value Fit Question - A',
                'Onsite Value Fit Question - B',
                'Onsite Value Fit Question - C',
                'Onsite Value Fit Question - D'
            ) and score in ('1 - Srong No Hire', '2 - No Hire')
            group by interview_name
        ) onsite_fit_question_not_hire
        on onsite_fit_question_not_hire.interview_name = onsite_fit_question.interview_name
        ;
    """
    return server._execute_extract(query)


def get_tag_candidate_overview(server: Server) -> pd.DataFrame:
    query = """
        select distinct ct.tag, "Candidate Rejected the offer", "Candidate Accepted the offer"
        from hiring_process.candidate_tags as ct
        full join (
            select 
                count(distinct o.candidate_id)  as "Candidate Rejected the offer",
                ct.tag 
            from hiring_process.offers as o
            inner join hiring_process.candidate_tags ct
            on ct.candidate_id = o.candidate_id
            where o.candidate_id not in (
                select candidate_id from hiring_process.offer_accepts as oa
            )
            group by ct.tag
        ) as o 
        on o.tag = ct.tag
        full join (
            select
                count(distinct o.candidate_id) as "Candidate Accepted the offer",
                ct.tag 
            from hiring_process.offers as o
            inner join hiring_process.candidate_tags ct
            on ct.candidate_id = o.candidate_id
            where o.candidate_id in (
                select candidate_id from hiring_process.offer_accepts as oa
            )
            group by ct.tag
        ) oa
        on ct.tag = oa.tag;
    """
    return server._execute_extract(query).fillna(0)

def get_inferviews_table(server: Server) -> pd.DataFrame:
    return server.db['hiring_process'].tb['interviews'].download()

