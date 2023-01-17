CREATE KEYSPACE IF NOT EXISTS clinic
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE clinic;


CREATE TABLE doctor (
  last_name text ,
  specialization text,
  avability set <text>,
  work_start time,
  work_end time,
  PRIMARY KEY (last_name, specialization)
);

CREATE TABLE doctor_visits (
  last_name text,
  m_day date,
  visit_time time,
  visit_uuid timeuuid,
  ss_num text,
  patient_last text,
  PRIMARY KEY ((last_name, m_day), ss_num)
);
CREATE INDEX ON doctor_visits (ss_num);

CREATE TABLE patient (
  first_name text,
  last_name text,
  ss_num text,
  PRIMARY KEY (ss_num)
);

CREATE TABLE visits (
  visit_uuid timeuuid,
  patient_last text,
  m_day date,
  visit_time time,
  ss_num text,
  doctor_last text,
  PRIMARY KEY ((ss_num, m_day), doctor_last)
  );

  CREATE INDEX ON visits (ss_num);