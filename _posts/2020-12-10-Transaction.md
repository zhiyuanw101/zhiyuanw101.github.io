---
layout: post
title: Transaction
categories: [DBMS, Wiki]
description: Transaction in DBMS
keywords: DBMS
---

## ACID

- Atomicity: All actions in transaction happen or none of them happen
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
  - determine serializable:
    - Read/ Write value matters
    - assign value to guarantee
    - **View serializability**
      - make sure consistent
      - view equivalent to serial schedule
      - View equivalent:
        - **Initial Read**: If T1 reads an initial value A in S1, then T1 must also read that same initial value A in S2.
        - **Updated Read**: If T1 reads a value A' written by T2 in S1, then T1 must also read the same value A' written by T2 in S2.
        - **Final Write operation**: If the transaction T1 is the last to write A'' in S1, then T1 must also be the last to write A'' in S2.


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

#### Conflict serializable

- **conflict equivalent**:
  - involve same transactions
  - order each pair of conflicting operations in the same way
- **conflict serializable**: conflict equivalent to serial schedule
  - **conflict serializable** ==> **serializable**
  - *Theorem:* **conflict serializable** <==> precedence graph is **acyclic**
    - equivalent serial schedule given by any topological sort over graph


### Recoverability

- **Recoverable schedule**: Transaction commit only after all transactions whose changes they have read commit
  - don't commit until all changes read have committed, such that if one of the changes is aborted, we could abort
  - could have cascade aborts

- **Avoid cascading aborts (ACA)**: Transaction only read changes of committed transactions
  - **ACA** ==> **Recoverable**
  - no aborts

### Locking

- types:
  - **shared** lock: read
  - **exclusive** lock: write

- **Two-Phase Locking (2PL)**
  - **2PL**:
    - T release any lock, it can acquire no new lock
    - Guarantee **conflict-serializability**
      - equivalent schedule given order in which transactions enter shiring phase
  - **Strict 2PL (S2PL)**:
    - Hold **exclusive locks** till end of Xact
    - Guarantee **conflict-serializability** and **ACA**
  - **Strong Strict 2PL (SS2PL)**:
    - Hold **all locks** till end of Xact
    - simpler implemetation

- Implementation: **Lock Table**
  - Hash table of Lock Entries
- **Deadlock**
  - 4 conditions:
    - Mutual Exclusion
    - Hold and wait
    - No Pre-emption
    - Circular wait
  - Detection:
    - waits-for graph
    - time-outs
  - Prevention:
    - assign priorities to transactions
      - wait-die
      - wound-wait

## Recovery

- use memory as cache
  - problems: (on crash)
    - pages writes of commited (redo)
    - pages writes of uncommited (undo)
  - solution:
    - invariant:
      - FORCE: to disk upon COMMIT
      - NOT STEAL: do not evict UNCOMMITED pages
    - **ARIES**:
      - supports FORCE & NOT STEAL
      - every update write:
        - database page
        - transaction log
          - help undo/redo
      - Log:
        - Entries:
          - Log Sequence Number (LSN)
          - XID: transaction id
          - type: update/commit/abort/**CLRs**
          - prevLSN
          - page\#, offset, size
          - prev-image, new-image
        - also log commit/abort
      - **Write-Ahead Logging** (WAL)
        - update log record **before** data page to disk
        - wirte all log records for Xact before **commit**
        - gurantee:
          - atomicity
          - durability
      - **Compensating Log Records** (CLRs)
        - describe update about to be **undone** (due to abort), write to log before undo