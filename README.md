# Praca inżynierska PUT-DB-2023 - Backend
Backend prototypowego systemu wspomagającego zarządzanie infrastrukturą bazodanową do prowadzenia zajęć laboratoryjnych.

## Uruchamianie
Aby uruchomić projekt należy wykonać następujące kroki:
1. Zainstalować [Docker Desktop](https://www.docker.com/products/docker-desktop/) (polecane) lub [Docker Engine](https://docs.docker.com/get-docker/) (wymaga osobnej instalacji [Docker Compose](https://docs.docker.com/compose/install/)).
2. Uruchomić polecenie `docker-compose up` w głównym katalogu projektu.
3. W celu dostępu do API należy otworzyć http://localhost:8000/api/ w przeglądarce i zalogować się przez [frontend](https://github.com/PUT-DB-2023/frontend) aplikacji lub poprzez wykonanie zapytania POST pod adres http://localhost:8000/api/login z danymi logowania (np. z użyciem Postmana):
```JSON
{
    "email": "admin@cs.put.poznan.pl",
    "password": "admin"
}
```
