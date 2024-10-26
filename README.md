# DataContracts - Data Quality - TechTalk

---

## Why DataContracts

What problems are we trying to solve with DataContracts?

* Create clarity and unambiguously describe _information_.
* Have a _single_ document/specification that can be used both by humans AND computers (no more/less trying to recreate in code what has been written down somewhere already for humans)
* Make a _Data Sharing Agreement_ between a _Data Producer_ and a _Data Consumer_ tangible and in an usable format from an IT perspective.

---

## What are DataContracts

So what are DataContracts?

```yaml
dataContractSpecification: 0.9.3
id: urn:datacontract:checkout:orders-latest
info:
  title: Orders Latest
  version: 1.0.0
  description: |
    Successful customer orders in the webshop. 
    All orders since 2020-01-01. 
    Orders with their line items are in their current state (no history included).
  owner: Checkout Team
  slackChannel: "#checkout"
  contact:
    name: John Doe (Data Product Owner)
    url: https://teams.microsoft.com/l/channel/example/checkout
tags:
  - checkout
  - orders
  - s3
...
```

---

## The different parts of a DataContract

## Data Quality checks

### SodaCL

---

## Other benefits of DataContracts

## When and where to use

---

## The End

And where to find more information:

* [Data Contracts](https://datacontract.com/)
* [Data Contract CLI](https://github.com/datacontract/datacontract-cli)
* [Soda Check Language](https://docs.soda.io/soda-cl/soda-cl-overview.html)
