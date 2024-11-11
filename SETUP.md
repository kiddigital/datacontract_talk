# Setup environment

Setup your local enviroment to follow the tutorial.

## Prerequisits

You need at least to following to get started

* a Python 3 environment on your local machine
* a good IDE like VisualStudioCode or PyCharm

## Installation

* Create a Python virtual environment to install the needed Python modules

```bash
python3 -m venv .dcdqenv
```

* Activate the Virtual Enviroment

```bash
source .dcdqenv/bin/activate
```

* Install the required Python packages

```bash
pip3 install datacontract-cli[all]
```

```bash
pip3 install soda-core-postgres
```

```bash
pip3 install -r requirement.txt
```


export DATACONTRACT_POSTGRES_PASSWORD=Enex1s2024
export DATACONTRACT_POSTGRES_USERNAME=exsnet

## PostgreSQL

sudo apt install postgresql-client

datacontract export --format=sql dcdqexample.datacontract.yaml | psql -h localhost -U exsnet -f -
psql -h localhost -U exsnet -f exampledata.sql


## Podman

https://hub.docker.com/_/postgres

podman pull postgres
podman run -e POSTGRES_PASSWORD=Enex1s2024 -e POSTGRES_USER=exsnet -d --name postgres -p 5432:5432 postgres
podman stop postgres

## Links

https://editor.datacontract.com/

https://gpt.datacontract.com/
https://chatgpt.com/g/g-QGMQrqm3p-data-contract-gpt
