# Sayna-TestFront-python3.7

-requirements:
-postgres, python 3.7 or ++

- git clone https://github.com/enricfranck/Sayna-TestFront-python3.7

-python3.7 -m venv venv

-run pip install -r rquirements.txt

-cd backend/

-create a file .env

-past this:

USE_SQLITE_DB: False

POSTGRES_DB: mydb

POSTGRES_USER:postgres

POSTGRES_PASSWORD:postgres

POSTGRES_SERVER: localhost

POSTGRES_PORT:5432

SECRET_KEY=testsaynanovembre!!

run uvicorn main:app --reload
