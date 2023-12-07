# Commands

Most of these commands ran on the terminal at the root of the project.

## Initial project setup
```shell
$ mkdir internetwithviet
$ cd internetwithviet
$ python3.11 -m venv venv
$ venv/bin/pip install --upgrade pip setuptools
$ venv/bin/pip install pdm
$ venv/bin/pdm init
$ venv/bin/pdm add "litestar[full]"
$ env/bin/alembic init alembic
$ sqlite3 internetwithviet.db
$ venv/bin/alembic revision --autogenerate -m "create quotes table"
$ touch src/app.py
```