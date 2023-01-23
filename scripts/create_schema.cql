-- Tables created to fulfill there queries:
-- doctors data, when they work how long etc
-- patient basic data
-- visits scheduled to specific doctor at this day
-- visits scheduled by this specific patient
-- visits_by_patient and visits_by_doctor should have same size at the end

CREATE KEYSPACE IF NOT EXISTS clinic
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };

USE clinic;

CREATE TABLE doctor (
  doctor_surname text ,
  avability set <text>,
  work_start time,
  work_end time,
  specialization text,
  PRIMARY KEY (doctor_surname)
);

CREATE TABLE visits_by_doctor (
  doctor_surname text,
  m_day date,
  visit_time time,
  visit_uuid timeuuid,
  ss_num text,
  patient_surname text,
  description text,
  PRIMARY KEY ((doctor_surname, m_day), visit_uuid, ss_num)
);
CREATE INDEX ON visits_by_doctor (doctor_surname);
CREATE INDEX ON visits_by_doctor (ss_num);
-- Indexes created for debugging purposes

CREATE TABLE patient (
  first_name text,
  patient_surname text,
  ss_num text,
  PRIMARY KEY (ss_num)
);

-- visits_by_patient to improve read query

CREATE TABLE visits_by_patient (
  doctor_surname text,
  m_day date,
  visit_time time,
  visit_uuid timeuuid,
  ss_num text,
  patient_surname text,
  description text,
  PRIMARY KEY (ss_num, m_day, visit_uuid)
  )
  WITH CLUSTERING ORDER BY (m_day DESC);