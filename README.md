# DataContracts - Data Quality - TechTalk

+-------------------+                      +-------------------+
|   Data Producer   |                      |                   |
|                   |  sends data          |                   |
|   +-----------+   |  ------------------> |                   |
|   |  Data     |   |   DataContract       |                   |
|   |  Source   |   |   (Schema) defines   |   +-----------+   |
|   |           |   |   structure and      |   |           |   |
|   |  (e.g.    |   |   quality            |   |           |   |
|   |  API, DB) |   |   (expectations)     |   |  Data     |   |
|   +-----------+   |   of data            |   |  Consumer |   |
+-------------------+                      |   |           |   |
                                           |   |           |   |
                                           |   |           |   |
                                           +-------------------+
                                                     |
                                                     |
                                        DataContract provides structure
                                        and is useable for Data Quality

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
The above shows a part of an example _dataContract_.

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
The above shows a part of the _v1.1.0 dataContractSpecification_.

---
The advantage of using JSON-schema to describe the contract specification is that JSON-schema is a widely supported way to describe data and its structure.
Nowadays a lot of tools, code-libraries, etc. have support for JSON-schema.

JSON-schema's allow the seperation between the _data (and its structure) itself_ and the _specification of the data (and its structure)_.
(Similar to what XML-Schema Definitions (XSD's) did for XML back in the days)

The specification is _declarative_ (describes _what_) and can be used within code 
_without_ the need to code-out all the details on _how_ to work with the data and its structure ( _imperative_ code).

As JSON (JavaScript Object Notation) and YAML (Yet Another Markup Language) are interchangable from a computer processing perspective,
JSON-schema works for both for JSON and YAML. It does not matter if data uses the JSON format or YAML format.

So by using YAML as the format to descibe Data Contracts, JSON-schema can still be used to describe (and validate) data contracts,
But YAML also makes a written Data Contract much more _human readable_.




NOTE: An often heard 'issue' of YAML (in the development community) is that it isn't easy to 'work with YAML' as it is for example _indentation sensitive_.
Although true, it isn't hardly an issue anymore as today's IDE's and other YAML editors assist 'YAML coders' with sufficient syntax support.
And the readability aspect of YAML is beyond doubt compared to the 'verbose and on-screen complexity' of JSON.

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
Similar to a piece of code, a piece of DDL, an ER-diagram, etc., the _Model_ describes the data and its structure.

```yaml
models:
  netstation:
    description: Contains details of the net station, including its location and ID
    type: table
    fields:
      marid:
        description: Unique identifier for the NetStation
        required: true
        $ref: "file://exsreferences.yaml#/definitions/marid"
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
The above shows a part of a _Model block_ of a Data Contract describing the model with its _Fields_.


NOTE: A Data Contract can contain more that 1 Model!

---

## Model Fields

A Model is based on a set of _Fields_:
```yaml
    fields:
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
- how it looks like using examples
- if and how the fields should be handled from a Privacy perspective
- and much more (optionally even custom attributes)




You can use [Data Contract GPT](https://chatgpt.com/g/g-QGMQrqm3p-data-contract-gpt) to quickly get an initial Data Contract with model from most (pieces of) data sets.

---

## Re-using Field definitions

Often, certain _Fields_ are used in multiple models and/or contracts.
Instead of re-declaring it again and again, it is possible to create a _$ref_ to a location that declares it once.

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
Above a _definitions_ block that can be referenced from within model(s).

The _reference_ can be a reference to another piece in the current Data Contract or
can be a reference to another document.

```yaml
      marid:
        description: Unique identifier for the NetStation
        required: true
        $ref: "file://exsreferences.yaml#/definitions/marid"
```

NOTE: automatical de-refenencing of references to external files (eihter local or via URL's) is not always supported by all tools that can work with JSON-schema.
It is supported by the 'datacontract-cli' and library.

---

## Data Quality

A lot of _Field_ attributes can be used to check quality of data.
Some attributes are:
- format
- pattern (regexp)
- enum
- minLength/maxLength
- minimum/maximum
- precision/scale

```yaml
      installdate:
        type: string
        required: true
        format: date
        description: Date when the NetStation become operational
      stationtype:
        type: string
        required: true
        description: Type of the NetStation
        enum:
          - Netstation
          - Klantstation
```
Some examples of attributes that can be used for Data Quality purposes.

---

## Governance - Privacy and Security

But also _Privacy and Security_ attributes can be set. For example:
- pii
- classification

```yaml
      manufacturer:
        type: string
        description: Manufacturer of the transformer
        pii: true
        classification: confidential
        tags:
          - hlin#asset_manufacturer_name
          - conflevel#2
```
By adding _tags_, additional context can be provided to use downstream when processing the data in a Data Contract.

Examples:
- The 'conflevel#2' tag could provide additional details on how data with the _classification: confidential_ should be handled.
- Using the 'hlin#asset_manufacturer_name' tag, information can be added for _horizontal lineage_ purposes.
  (here linking this field to the 'business level definition' of 'asset_manufacturer_name')

---

## More Data Quality - SodaCL, Great Expectations, SQL, etc.

Next to defining the attributes of Fields, which can be used to validate if data complies with its definitions,
additional, and more complex, data quality checks can be defined and executed.

A special _Quality_ block can be defined both on _Field_ and/or _Model_ level.

```
    quality:
      - type: sql
        description: The Installdate should be after 01-01-2020
        query: |
          select extract(epoch from (to_date(installdate, 'DD-MM-YYYY'))) as lifetime
          FROM {model}
        mustBeGreaterThan: 1577833200
```
Above a _Model level Quality block_ using SQL to define the check.

NOTE: Although the recent 1.1.0 spec has support for this, it does not fully work yet with the datacontract-cli
as the latest version of the cli does not fully support 1.1.0 (it does/did with 0.9.3)

Integration with different Data Quality engines like _Soda_ (Using SodaCL) or _Great Expectations_ is under development.
The latest 1.1.0 specification has support at the level of the Spec itself, but for example the 'datacontract-cli' does not fully support these engines yet (under development).
This is something that should be relatively easy to be added when developing solutions leveraging Data Contracts (and these DQ engines).

---

## Governance metadata

The Data Contract can hold a lot/most of the relevant information needed from a Data Governance perspective.

Generic information about the Data Contract:
```yaml
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
```

Terms
```yaml
terms:
  usage: |
    Data can be used for reports, analytics and machine learning use cases.
    Information may be linked and joined by other tables
  limitations: |
    Not suitable for real-time use cases.
    Data may not be used to identify individual customers.
    Max data processing per day: 10 TiB
  billing: free
  noticePeriod: P18M
```
This _terms_ block contains the _terms of the agreement between Publisher and Consumer_.

The _info_ block provides information about the _Publisher_. 

Ideally, there is a system that keeps track of which _Consumers_ have been granted access to certain data by Producers.
An Open Source initiative can be found at [datacontract-manager.com](https://www.datacontract-manager.com/)

---

## Governance metadata - Continued

ServiceLevels provide very useful further context on the conditions of use for the data.

```yaml
servicelevels:
  availability:
    description: The server is available during support hours
    percentage: 99.9%
  retention:
    description: Data is retained for two years
    period: P2Y
    unlimited: false
  latency:
    description: Data is available within 1 month after the Net Station is operational
    threshold: 1M
    sourceTimestampField: netstation.installdate
    processedTimestampField: netstation.installdate
  freshness:
    description: The age of the youngest row in a table.
    threshold: 25h
    timestampField: netstation.installdate
  frequency:
    description: Data is delivered once a day
    type: batch # or streaming
    interval: daily # for batch, either or cron
    cron: 0 0 * * * # for batch, either or interval
  support:
    description: The data is available during typical business hours at headquarters
    time: 9am to 5pm in CST on business days
    responseTime: 1h
  backup:
    description: Data is backed up once a week, every Sunday at 0:00 UTC.
    interval: weekly
    cron: 0 0 * * 0
    recoveryTime: 24 hours
    recoveryPoint: 1 week
```
Above a _Service Level_ block explaining what can be expected from the data for which the Data Contract applies.

Special attention for _retention_ stating how long history is kept of the data. Often forgotten!!
(and now ready to be automated!)

---

## Special attention - (Field) Types

By default the _Data Contract Specification_ supports the standard JSON-schema types.
But some systems have additional and/or more specialized types.
Those systems need to know how to work with the given type when not unambigious.

```yaml
    fields:
      my_field_1:
        description: Example for AVRO with Timestamp (millisecond precision)
        type: timestamp
        example: 1970 00:00:00.000 UTC
        config:
          avroType: long
          avroLogicalType: timestamp-millis
          snowflakeType: timestamp_tz
```
Above field has an additional (and optional) _config_ block in which system specific types are mentioned.
This way, when this field is used within an 'AVRO' object or within a 'SnowFlake' environment,
these systems have information on how they should handle the _timestamp_ type.

---

## When and where to use

So, where and when to use:

* When discussing about what data to use, what is means, etc. -> great way to document things

* In your application -> leverage the Data Contract (declarative) instead of programming everything (imperative).
  Makes your code more readable, easier to adapt to changes (as they can just be newer versions of the Data Contract), etc.)

* In your Data Pipeline -> similar to code, use the Data Contract to check the data you are processing.

* To help yourself in fulfilling the Data Governance needs.

* ...


## Other benefits of DataContracts

Data Contract could be usable to populate Data Governance tools like Erwin Data Intelligence or Collibra, etc.
(Or vice versa if the Data Governance tool would support the generation/management of Data Contracts).

Although I haven't found any working examples yet :) (Oktober 2024)

---

## The End

Final remarks:
- Data Contracts are a very promising way to make Data Governance workable and integral part of building IT systems.

- Current initiatives like 'datacontracts.com' with its 'Data Contract Specification' are NOT feature compleet anno 2024.

- But it is already very usable. Not everything can be fully automated yet (at least not without additional development).

- By starting to adopt 'Data Contracts', it forces Business and IT aligment on many aspects
  and in a way that is future-proof to support further Data Governance automation!




Where to find more information:

* [Data Contracts](https://datacontract.com/)
* [Data Contract Editor](https://editor.datacontract.com/)
* [Data Contract CLI](https://github.com/datacontract/datacontract-cli)
* [Data Contract GPT](https://gpt.datacontract.com/)

* [The schema specification for Data Contracts](https://github.com/datacontract/datacontract-specification/blob/main/datacontract.schema.json)
  (can also be found in the [JSON Schemastore](https://www.schemastore.org/json/), search for 'data contract specification')

* [Soda Check Language](https://docs.soda.io/soda-cl/soda-cl-overview.html)
