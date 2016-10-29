# AgileBoardProject
Agile Board Project for CSE412

## Setup (for local use)
1. Install [docker](https://www.docker.com/)
2. Install Python.
3. Install pip (might just come with Python nowadays, run `pip --version` to check)
4. Install postgres on your machine.
5. `pip install psycopg2` for ability to use Python-Postgres interface
6. Clone this git repository to somewhere on your machine `git clone https://github.com/spencerbyw/AgileBoardProject.git`
7. Make sure docker is running. Fire off the following commands:
  - `docker pull postgres` get the postgres image
  - `docker run -d -p 5432:5432 postgres` starts a postgres process in the background, exposing port 5432 so we can use it
8. Inside the git repository, run the following commands:
  - `make from_scratch` This will load the database in the docker container with test data
9. You now have a the database working locally.

## Usage
### To Use psql
To use `psql`, the command line interface for Postgres, do the following:
- `docker ps -a` and copy the name of the running container (should be some weird name like "ecstatic_hugle")
- `docker run -it --rm --link <NAME_THAT_YOU_COPIED>:postgres postgres psql -h postgres -U postgres` This will give you access to psql command line interface. You can now run commands here.
- Useful commands:
  - `\q` Use this to quit psql
  - `\dt` List all tables
  - Run whatever SQL query you want, like `select * from card;`


## Authors
- Spencer Bywater [@spencerbyw](https://github.com/spencerbywater)
- Alex Rhodes
- Alex Chambers
- Caleb Hutchison
