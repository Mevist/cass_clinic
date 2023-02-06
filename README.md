#cass_clinic
System rejestracji pacjentów do przychodni używając Cassandry.
# Symulacja przychodni 
Projekt symuluje rejestracje wizyt pacjentów u lekarzy w pewnej przychodni z wykorzystaniem bazy danych Cassandra. Pacjent może zarejestrować się w przychodni, zarejestrować wizytę do danego lekarza, w danym dniu.
Jeśli już jest zarejestrowany, to może zaktualizować godzine wizyty. Maksymalny czas wizyty jest odgórnie ustawiony na 30 minut, taki też czas musi minąc pomiędzy kolejnymi
wizytami.

# Uruchomienie środowiska
W celu utworzenia środowiska z wieloma węzłami wykorzystano Minikube. Domyślnie Minikube uruchamia sie 2GB pamięci i 2 CPUs dlatego zaleca się uruchomienie go z wiekszą iloscia zasobów:
```
minikube start --memory 4096 --cpus 4
alias kubectl='minikube kubectl --'
kubectl apply -f cass_minikube.yml
```
Aby podłączyć system do bazy danych lokalnie należy poczekać aż wstaną wszystkie pody i przekierować porty
```
kubectl get sts --watch
kubectl port-forward service/cassandra 9042:9042
```
Dodanie stworzenie tabel i załadowanie podstawowych danych do bazy z folderu scripts
```
cqlsh -f ./create_schema.cql
cqlsh -f ./load_data.cql
```
Wyczyszczenie tabel bazy danych
```
cqlsh -f ./drop_schema.cql
```
Uruchomienie aplikacji konsolowej i obsługa
```
/bin/python3.8 /home/srds/cass_clinic/main.py
```
Z menu możemy się zarejestrować lub zalogować jako jakiś pacjent. Możemy uruchomić stress test generując defaultowo 250 pacjentów którzy cały czas rejestrują nowe wizyty albo
podglądają juz wizyty zarejestrowane.

Przykładowe zapytania do bazy danych za pomocą narzedzia cqlsh
```
cqlsh
cqlsh USE clinic;
```
```
SELECT * FROM patient;
SELECT * FROM doctor;
SELECT * FROM visits_by_doctor WHERE doctor_surname='Kowalski' AND m_day='2023-01-12';
SELECT * FROM visits_by_patient WHERE ss_num='9909290';
```
