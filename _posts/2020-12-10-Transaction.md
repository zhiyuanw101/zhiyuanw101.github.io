---
layout: post
title: Transaction
categories: [DBMS, Wiki]
description: Transaction in DBMS
keywords: DBMS
---

## ACID

- Atomicity: All actions in transaction happen or not happen
- Consistency: consistent DB + consistant transaction => consistent DB
- Isolation: Execution of transaction is isolated from other transaction
- Durability: If a transaction commits, its effects persist
  
## Schedule

An interleaving of actions from a set of transactions

### Elements

- Read(X)
- Write(X)
- Commit
- Abort

### Definitions

- **Complete Schedule**: Each transactions ends in commit or abort
- **Serial Schedule**: No interleaving actions among transactions
- **Serializable Schedule**: Final state equal to some **complete serial schedule** of committed transactions.

### Conflict & Anomalies

- Conflict not necessarily anomaly
- Conflict:
  - **Write-Read (WR)**
    - reading uncommitted change

    | T1     	| T2     	|
    |--------	|--------	|
    | R(A)   	|        	|
    | W(A)   	|        	|
    |        	| R(A)   	|
    |        	| W(A)   	|
    |        	|  R(B)  	|
    |        	| W(B)   	|
    |        	| commit 	|
    | R(B)   	|        	|
    | W(B)   	|        	|
    | commit 	|        	|

  - **Read-Write (RW)**
    - Unrepeatable read

    | T1     	| T2      	|
    |--------	|---------	|
    | R(A)   	|         	|
    |        	| W(A)=95 	|
    | R(A)   	|         	|
    | W(A)   	|         	|
    | commit 	|         	|
    |        	| commit  	|

  - **Write-Write (WW)**
    - Overwriting uncommitted changes

    | T1      	| T2      	|
    |---------	|---------	|
    | W(A)=90 	|         	|
    |         	| W(A)=95 	|
    |         	| W(B)=95 	|
    | W(B)=90 	|         	|
    | commit  	|         	|
    |         	| commit  	|

