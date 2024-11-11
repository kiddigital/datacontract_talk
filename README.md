# DataContracts - Data Quality - TechTalk

+-------------------+                 +-------------------+
|   Data Producer   |    --->         |                   |
|                   |  sends data     |                   |
|   +-----------+   |  -------------->|                   |
|   |  Data     |   |    DataContract |                   |
|   |  Source   |   |    (Schema)     |   +-----------+   |
|   |           |   |    defines      |   |           |   |
|   |  (e.g.    |   |    structure    |   |           |   |
|   |  API, DB) |   |    of data      |   |  Data     |   |
|   +-----------+   |                 |   |  Consumer |   |
+-------------------+                 |   |           |   |
                                      |   |           |   |
                                      |   |           |   |
                                      +-------------------+
                                              |
                                              |
                                DataContract provides structure

---

## Why DataContracts

What problems are we trying to solve with DataContracts?

* Create clarity and unambiguously describe _information_.
* Have a _single_ document/specification that can be used both by humans AND computers.
  (no more/less trying to recreate in code what has been written down somewhere already for humans)
* Make a _Data Sharing Agreement_ between a _Data Producer_ and a _Data Consumer_ tangible and in a usable format from an IT perspective.
* Making _Data Governance_ into something doable and usable :)

---

## What are DataContracts

So what are DataContracts?

Basically, a pre-defined specification on how to write a _datacontract_.

The 2 main specifications are _open data contract specification_ (latest is v3.0) and _data contract specification_ (latest is v1.1.0) 

```yaml
dataContractSpecification: 1.1.0
id: urn:datacontract:nbility:2.2:grid:grid-component:primairy-component:netstation:0.2.0
info:
  title: Net Station
  description: Net Station data for low and medium voltage grids
  version: 0.2.0
  license: https://creativecommons.org/licenses/by-nd/3.0/nl/
  owner: Enexis - EDSN
  status: proposed
  contact:
    name: Patrick Beitsma (Systems Architect)
    url: https://www.enexis.nl
    email: patrick.beitsma@enexis.nl
tags:
  - enexis
  - nbility
  - grid component
  - primaire grid component
  - netstation
links:
  schemaurl: https://schemas.enexis.nl/datacontracts/netstation/0.2.0/netstation.datacontract.yaml
servers:
  localdevelopment:
    type: postgres
...
```
The above shows a part of an example _dataContractSpecifiation_.

---
Both specifications make use of _JSON-schema_ to describe the specification itself.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "DataContractSpecification",
  "properties": {
    "dataContractSpecification": {
      "type": "string",
      "title": "DataContractSpecificationVersion",
      "enum": [
        "1.1.0",
        "0.9.3",
        "0.9.2",
        "0.9.1",
        "0.9.0"
      ],
      "description": "Specifies the Data Contract Specification being used."
    },
    "id": {
      "type": "string",
      "description": "Specifies the identifier of the data contract."
    },
    "info": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title of the data contract."
        },
        "version": {
          "type": "string",
          "description": "The version of the data contract document (which is distinct from the Data Contract Specification version)."
        },
        "status": {
          "type": "string",
          "description": "The status of the data contract. Can be proposed, in development, active, retired.",
          "examples": [
            "proposed",
            "in development",
            "active",
            "deprecated",
...
```

---
The advantage of using JSON-schema to describe the contract specification is that JSON-schema is a widely supported way to describe data and its structure.
Nowadays a lot of tools, code-libraries, etc. have support for JSON-schema.

JSON-schema's allow the seperation between the _data (and its structure) itself_ and the _specification of the data (and its structure)_.
(Similar to what XML-Schema Definitions (XSD's) did for XML back in the days)

The specification is _declarative_ (describes _what_) and can be used within code _without_ the need to code-out all the details on _how_ to work with the data and its structure ( _imperative_ code).

As JSON (JavaScript Object Notation) and YAML (Yet Another Markup Language) are interchangable from a computer processing perspective,
JSON-schema works for both for JSON and YAML. It does not matter if data uses the JSON format or YAML format.

So by using YAML as the format to descibe Data Contracts, JSON-schema can still be used to describe (and validate) data contracts,
But YAML also makes a written Data Contract much more _human readable_.

---

## The different parts of a DataContract

A Data Contract consist of a number of parts that make up the contract:

+ ID
+ Info block
+ Server block
+ Terms
+ Model(s)
+ Definitions
+ ServiceLevels

The different blocks can (and should) contain a lot of very useful information describing numerous _Data Governance_ aspects.
And as these aspects are written in a structured way, using a computer readable format,
the data of these aspects can be used to automate all kind of Data Governance tasks.

---

## The Model

This is where it starts.
Similar to an ERD, a piece of code, a piece of DDL, etc., the _Model_ describes the data and its structure.

```yaml
models:
  netstation:
    description: Contains details of the net station, including its location and ID
    type: table
    fields:
      marid:
        description: Unique identifier for the NetStation
        required: true
        $ref: "#/definitions/marid"
        quality:
          - type: custom
            description: The MARID should be unique
            engine: soda
            implementation:
              type: no_duplicate_values
      rdpoint:
        description: Geographic location of the NetStation
        required: true
        $ref: "#/definitions/rdpoint"
      installdate:
        type: string
        required: true
        format: date
        description: Date when the NetStation become operational
      manufacturer:
        type: string
        description: Manufacturer of the transformer
        pii: true
        classification: confidential
      stationtype:
        type: string
        required: true
        description: Type of the NetStation
        enum:
          - Netstation
          - Klantstation
```

A Data Contract can contain more that 1 Model!

---

A Model is based on a set of _Fields_:
```yaml
      rdpoint:
        description: Geographic location of the NetStation
        required: true
        $ref: "#/definitions/rdpoint"
      installdate:
        type: string
        required: true
        format: date
        description: Date when the NetStation become operational
```
The _Field_ describes the attributes and characteristics of a field.

Attributes that state 
- if the field is _required_ or not, 
- what is the _type_ of the field
- gives a _description_ of the field
  (which is very useful information to give more clarity on the business meaning of the field! A _Data Governance_ thing!)

Often, certain _Fields_ are used in multiple contracts. Instead of re-declaring it again and again, it is possible to create a _$ref_ to a location that declares it once.

```yaml
definitions:
  rdpoint:
    ID: "geospatial/rdpoint"
    title: Rijksdriehoekspunt
    description: |
      A Rijksdriehoekspunt (RD point) is a geographic coordinate system used in the Netherlands.
    type: string
    pattern: ^[0-9]{6}\,[0-9]{2,3}.[0-9]{6}\,[0-9]{2,3}$
    examples:
    - "275939,493.583845,199"
```

You can use [Data Contract GPT](https://chatgpt.com/g/g-QGMQrqm3p-data-contract-gpt) to quickly get an initial Data Contract with model from most (pieces of) data sets.

---

## Data Quality checks

- format
- pattern (regexp)
- enum

```yaml
      installdate:
        type: string
        required: true
        format: date
        description: Date when the NetStation become operational
      manufacturer:
        type: string
        description: Manufacturer of the transformer
        pii: true
        classification: confidential
      stationtype:
        type: string
        required: true
        description: Type of the NetStation
        enum:
          - Netstation
          - Klantstation
```

But also _Privacy and Security_ attributes can be used like:
- pii
- classification

---


### SodaCL

## Governance metadata

---

## Other benefits of DataContracts

## When and where to use

---

## The End

And where to find more information:

* [Data Contracts](https://datacontract.com/)
* [Data Contract CLI](https://github.com/datacontract/datacontract-cli)
* [Soda Check Language](https://docs.soda.io/soda-cl/soda-cl-overview.html)
