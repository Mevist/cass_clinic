USE clinic;

INSERT INTO doctor (doctor_surname, avability, work_start, work_end) VALUES ('Nowak', {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'},'8:00:00', '16:00:00');
INSERT INTO doctor (doctor_surname, avability, work_start, work_end) VALUES ('Kowalski', {'Monday', 'Tuesday', 'Thursday', 'Friday'},'8:00:00', '14:00:00');
INSERT INTO doctor (doctor_surname, avability, work_start, work_end) VALUES ('Szczepan', {'Friday', 'Saturday'},' 7:00:00', '13:00:00');

INSERT INTO patient (first_name, patient_surname, ss_num) 
VALUES ('Pierre', 'Angeles', '9909001');
INSERT INTO patient (first_name, patient_surname, ss_num) 
VALUES ('Augustus', 'Carranza', '9906055');
INSERT INTO patient (first_name, patient_surname, ss_num) 
VALUES ('Brandi', 'Brenner', '9909290');
-- {8c857e1c-933f-11ed-a1eb-0242ac120002, 61eed7c8-9341-11ed-a1eb-0242ac120002});

INSERT INTO visits_by_patient (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Szczepan', '2023-01-13', '13:00:00', 61eed7c8-9341-11ed-a1eb-0242ac120002,'9909290' , 'Brenner');
INSERT INTO visits_by_doctor (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Szczepan', '2023-01-13', '13:00:00', 61eed7c8-9341-11ed-a1eb-0242ac120002,'9909290' , 'Brenner');

INSERT INTO visits_by_patient (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '09:00:00', 8c857e1c-933f-11ed-a1eb-0242ac120002, '9909290' , 'Brenner');
INSERT INTO visits_by_doctor (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '09:00:00', 8c857e1c-933f-11ed-a1eb-0242ac120002, '9909290' , 'Brenner');

INSERT INTO visits_by_patient (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '09:30:00', cb920168-9865-11ed-8a46-e74516c7ef1b, '9906055' , 'Carranza');
INSERT INTO visits_by_doctor (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '09:30:00', cb920168-9865-11ed-8a46-e74516c7ef1b, '9906055' , 'Carranza');

INSERT INTO visits_by_patient (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '10:00:00', d792b03e-9865-11ed-bcc2-4b33151328e9, '9909290' , 'Brenner');
INSERT INTO visits_by_doctor (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname)
VALUES ('Kowalski', '2023-01-12', '10:00:00', d792b03e-9865-11ed-bcc2-4b33151328e9, '9909290' , 'Brenner');
