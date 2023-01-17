USE clinic;

INSERT INTO doctor (last_name,specialization, avability, work_start, work_end) VALUES ('Nowak', 'Cardiology', {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'},'8:00:00', '16:00:00');
INSERT INTO doctor (last_name,specialization, avability, work_start, work_end) VALUES ('Kowalski', 'Cardiology', {'Monday', 'Tuesday', 'Thursday', 'Friday'},'8:00:00', '14:00:00');
INSERT INTO doctor (last_name,specialization, avability, work_start, work_end) VALUES ('Szczepan', 'Dermatology', {'Friday', 'Saturday'},' 7:00:00', '13:00:00');

INSERT INTO patient (first_name, last_name, ss_num) VALUES ('Maciej', 'Ziobr', '9909001');
INSERT INTO patient (first_name, last_name, ss_num) VALUES ('Ola', 'Kot', '9906055');
INSERT INTO patient (first_name, last_name, ss_num) 
VALUES ('Krzystof', 'Pies', '9909290');
-- {8c857e1c-933f-11ed-a1eb-0242ac120002, 61eed7c8-9341-11ed-a1eb-0242ac120002});

INSERT INTO visits (visit_uuid, patient_last, m_day, visit_time, ss_num, doctor_last)
VALUES (61eed7c8-9341-11ed-a1eb-0242ac120002,'Pies', '2023-01-13', '13:00:00', '9909290' ,'Szczepan');
INSERT INTO doctor_visits (last_name, m_day, visit_time, visit_uuid, ss_num, patient_last)
VALUES ('Szczepan', '2023-01-13', '13:00:00', 61eed7c8-9341-11ed-a1eb-0242ac120002,'9909290' , 'Pies');

INSERT INTO visits (visit_uuid, patient_last, m_day, visit_time, ss_num, doctor_last)
VALUES (8c857e1c-933f-11ed-a1eb-0242ac120002,'Pies', '2023-01-12', '09:00:00','9909290' ,'Kowalski');
INSERT INTO doctor_visits (last_name, m_day, visit_time, visit_uuid, ss_num, patient_last)
VALUES ('Kowalski', '2023-01-12', '09:00:00', 8c857e1c-933f-11ed-a1eb-0242ac120002, '9909290' , 'Pies');