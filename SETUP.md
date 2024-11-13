# Setup environment

Setup your local enviroment to start playing around with Data Contracts!

## Prerequisits

You need at least to following to get started

* a Python 3 environment on your local machine
* Podman (or Docker) to run local containers
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
pip3 install datacontract-cli[postgres]
```

```bash
pip3 install soda-core-postgres
```

* Setup a postgress Username and Password

```bash
export DATACONTRACT_POSTGRES_USERNAME=exsnet
export DATACONTRACT_POSTGRES_PASSWORD=Enex1s2024
```

## Podman

* Assuming _podman_ is installed to support local (Docker)containers, let's create and start a PostgreSQL container

```bash
podman pull postgres
podman run -e POSTGRES_PASSWORD=Enex1s2024 -e POSTGRES_USER=exsnet -d --name postgres -p 5432:5432 postgres
podman stop postgres
```

## PostgreSQL

* Let's install the PostgreSQL Client to access our PostgreSQL server and database

```bash
sudo apt install postgresql-client
```

* Now populate the PostgreSQL database using the Data Contract model and example data

```bash
datacontract export --format=sql dcdqexample.datacontract.yaml | psql -h localhost -U exsnet -f -
psql -h localhost -U exsnet -f exampledata.sql
```

---

## Data Contract CLI

* Validate (lint) the Data Contract

```bash
datacontract lint dcdqexample.datacontract.yaml
```

* Let's test the data against the contract

```bash
datacontract test dcdqexample.datacontract.yaml
```


## Links

https://hub.docker.com/_/postgres
https://editor.datacontract.com/
https://gpt.datacontract.com/ -> https://chatgpt.com/g/g-QGMQrqm3p-data-contract-gpt
