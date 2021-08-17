create schema hiring_process;

CREATE TABLE hiring_process.candidates (
  CANDIDATE_ID varchar(50) not null,
  created_at date not null DEFAULT CURRENT_TIMESTAMP
);
create unique index "candidates_id_idx" on hiring_process.candidates(
    CANDIDATE_ID
);

CREATE TABLE hiring_process.interviews (
  JOB_POSTING_NAME varchar(50) not null,
  INTERVIEW_NAME varchar(50) not null,
  CANDIDATE_ID varchar(50) not null,
  INTERVIEWER_ID varchar(50) not null,
  SCORE varchar(50) not null,
  CREATEDAT_MS date not null DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT FK_CANDIDATE FOREIGN KEY(CANDIDATE_ID) REFERENCES hiring_process.candidates (CANDIDATE_ID) ON DELETE CASCADE
);
create index "interview_id_idx" on hiring_process.interviews(
    JOB_POSTING_NAME, INTERVIEW_NAME, CANDIDATE_ID
);
create index "interview_cascade_idx" on hiring_process.interviews(
    JOB_POSTING_NAME, INTERVIEW_NAME, CANDIDATE_ID
);

CREATE TABLE hiring_process.candidate_tags (
  CANDIDATE_ID varchar(50) not null,
  TAG varchar(50) not null,
  created_at date not null DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT FK_CANDIDATE FOREIGN KEY(CANDIDATE_ID) 
  REFERENCES hiring_process.candidates (CANDIDATE_ID) ON DELETE CASCADE
);
create index "candidate_tags_delete_cascade_idx" on hiring_process.candidate_tags(CANDIDATE_ID, TAG);
create index "candidate_tags_id_idx" on hiring_process.candidate_tags(CANDIDATE_ID, TAG);

CREATE TABLE hiring_process.offers (
  CANDIDATE_ID varchar(50) not null,
  JOB_POSTING_NAME varchar(50) not null,
  created_at date not null DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT FK_CANDIDATE FOREIGN KEY(CANDIDATE_ID) 
  REFERENCES hiring_process.candidates (CANDIDATE_ID) ON DELETE CASCADE
);
create index "offers_delete_cascade_idx" on hiring_process.offers(CANDIDATE_ID, JOB_POSTING_NAME);
create index "offers_id_idx" on hiring_process.offers(CANDIDATE_ID, JOB_POSTING_NAME);


CREATE TABLE hiring_process.offer_accepts (
  CANDIDATE_ID varchar(50) not null,
  JOB_POSTING_NAME varchar(50) not null,
  created_at date not null DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT FK_CANDIDATE FOREIGN KEY(CANDIDATE_ID) 
  REFERENCES hiring_process.candidates (CANDIDATE_ID) ON DELETE CASCADE
);
create index "offer_accepts_delete_cascade_idx" on hiring_process.offer_accepts(CANDIDATE_ID, JOB_POSTING_NAME);
create index "offer_accepts_id_idx"  on hiring_process.offer_accepts(CANDIDATE_ID, JOB_POSTING_NAME);
