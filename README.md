# internetwithviet

## Install & Run

1. Install

```shell
$ python3.11 -m venv venv
$ venv/bin/python -m pip install --upgrade pip setuptools
$ venv/bin/python -m pip install pdm
$ venv/bin/pdm install
```

2. Run:

```shell
$ venv/bin/litestar --app src.app:app run --debug --reload
```

## Commands
[COMMANDS.md](./COMMANDS.md) contains important commands that helped create/edit this repository