CREATE KEYSPACE IF NOT EXISTS clinic
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

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
  PRIMARY KEY ((doctor_surname, m_day), visit_uuid)
);
CREATE INDEX ON visits_by_doctor (doctor_surname);

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


--   CREATE INDEX ON visits (ss_num);