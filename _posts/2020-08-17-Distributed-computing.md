---
layout: post
title: Distributed Computing
categories: [Wiki, Utils]
description: 分布式系统第一次接触
keywords: Wiki, Utils
---
## [Hadoop](https://blog.csdn.net/hguisu/article/details/7238925)

- Hadoop的核心组件分为：HDFS（分布式文件系统）、MapReduce（分布式运算编程框架）、YARN（运算资源调度系统）

  - [MapReduce](https://en.wikipedia.org/wiki/MapReduce)
  
    - **Map**: 
      - `Map(k1, v1) => list(k2, v2)`
      - map all `v1`s to the same node according to `k1`
    - **Shuffle**: 
      - Group all `v2`s associated with `k2` to `list(v2)`
      - shuffle `v2`s associated with same `k2` to the same node
    - **Reduce**: 
      - `Reduce(k2, list(v2)) ==> list(k3, v3)`
      - combine `v2`s 

    - parallel:
      - `k1` marks same nodes for maping, `k2` marks same nodes for reducing, distribute data to nodes, aggregate `k3` from different nodes
      - `(k2, v2), (k3, v3)` same domain, `(k1, v1)` a different domain
      - **user only cares about `Map` and `Reduce`**

  - HDFS

  - YARN
  - 其他组件

    - Hive
    - Hbase
  