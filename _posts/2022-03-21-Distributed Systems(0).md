---
layout: post
title: Distributed Systems (0)
categories: [Wiki, Distributed System]
description: knowledge base on distributed systems
keywords: Distributed system, Concurrent
---

## References

- [Stackoverflow](https://stackoverflow.com/questions/9762101/what-is-linearizability)
- [Wiki](https://www.wikiwand.com/en/Linearizability#:~:text=Linearizability%20is%20a%20strong%20correctness,an%20unexpected%20or%20unpredictable%20manner.)
- EECS 491 @ Umich

## Linearizability

### Definition

A history ![\sigma ](https://wikimedia.org/api/rest_v1/media/math/render/svg/59f59b7c3e6fdb1d0365a494b81fb9a696138c36) is *linearizable* if there is a linear order of the completed operations such that:

1. For every completed operation in ![\sigma ](https://wikimedia.org/api/rest_v1/media/math/render/svg/59f59b7c3e6fdb1d0365a494b81fb9a696138c36), the operation returns the same result in the execution as the operation would return if every operation was completed one by one in order ![\sigma ](https://wikimedia.org/api/rest_v1/media/math/render/svg/59f59b7c3e6fdb1d0365a494b81fb9a696138c36).
2. If an operation op1 completes (gets a response) before op2 begins (invokes), then op1 precedes op2 in ![\sigma ](https://wikimedia.org/api/rest_v1/media/math/render/svg/59f59b7c3e6fdb1d0365a494b81fb9a696138c36).[[1]](https://doi.org/10.1145%2F78969.78972)



In other words:

- its invocations and responses can be reordered to yield a sequential history;
- that sequential history is correct according to the sequential definition of the object;
- if a response preceded an invocation in the original history, it must still precede it in the sequential reordering.



This definition of linearizability is equivalent to the following:

- All function calls have a *linearization point* at some instant between their invocation and their response.
- All functions appear to occur instantly at their linearization point, behaving as specified by the sequential definition.

### Other Explanation

- https://stackoverflow.com/questions/9762101/what-is-linearizability
- From EECS 491 slides:
  - Total ordering of writes
  - Read returns last **completed** write (note: complete does not require receive a reply, it is when the entire system committed the write)

