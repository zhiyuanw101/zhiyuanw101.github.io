---
layout: post
title: Map Reduce
categories: [DBMS, Wiki, Distributed System, Parallel Computing]
description: Map Reduce
keywords: DBMS, Data, Computation
---
The following contents are partly based on [EECS484](https://dijkstra.eecs.umich.edu/kleach/eecs484/f20/) course materials from the University of Michigan. 
## MapReduce (Hadoop)

- Big Idea:
  - seperate work into phases: mapping, grouping, reducing
    - **Mapping**: turn data into (key, value) pairs
    - **Grouping**: put same key together
    - **Reducing**: combine value of same key
  - define phases such that multiple computers can work without communication
  - client provide: 
    - input data
    - Map() function/ program
    - Reduce() function/ program
- MapReduce server
  - 
- Key notes:
  - all pairs with **same key** go to **same reducer**
    - merge two tables: match with same key
    - aggregate in one table: count, max, min by key
  - reduce starts after all map finish
  - Client, worker, master communicate in real distributed sys?

## [Map-Reduce in MongoDB](https://docs.mongodb.com/v3.2/core/map-reduce/)

### [Map function](https://docs.mongodb.com/manual/reference/method/db.collection.mapReduce/#requirements-for-the-map-function)

```js
function() {
   ...
   emit(key, value);
}
```

- In the **map** function, reference the current document as **this** within the function.
- The **map** function should not access the database for any reason.
- The **map** function may optionally call `emit(key,value)` any number of times to create an output document associating key with value.

### [Reduce function](https://docs.mongodb.com/manual/reference/method/db.collection.mapReduce/#requirements-for-the-reduce-function)

```js
function(key, values) {
   ...
   return result;
}
```

- MongoDB will not call the **reduce** function for a key that has only a single value. The values argument is an array whose elements are the value objects that are “mapped” to the key.
- MongoDB can invoke the **reduce** function more than once for the same key. In this case, the previous output from the **reduce** function for that key will become one of the input values to the next **reduce** function invocation for that key.
  - The **reduce** function must return an object whose *type* must be **identical** to the *type* of the **value** emitted by the **map** function.
  - *Idempotent*:
    - `reduce( key, [ reduce(key, valuesArray) ] ) == reduce( key, valuesArray )`
- The **reduce** function should not access the database, even to perform read operations.

### [Examples in MongoDB](https://docs.mongodb.com/manual/tutorial/map-reduce-examples/)

### Notes
- type: 
  - type(value) = type(result) [reduce result]
  - type(values) = array<type(value)> [reduce input]
