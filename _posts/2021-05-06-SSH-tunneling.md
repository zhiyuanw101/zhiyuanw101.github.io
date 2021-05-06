---
layout: post
title: SSH Tunneling 实现内网穿透
categories: [SSH, Networks]
description: SSH Tunneling 实现内网穿透
keywords: SSH, Networks
---

### Recourses

- [利用ssh反向代理以及autossh实现从外网连接内网服务器](https://www.cnblogs.com/kwongtai/p/6903420.html)
- [内网穿透系列——SSH反向隧道 （最简单的内网穿透方案）](https://my.oschina.net/runescape/blog/1616031)
- [SSH Forwarding](https://zhiyuanw101.github.io/2021/01/08/SSH-Forwarding/)

### Requirements

- 内网服务器 A

  - user: inside

- 外网服务器 B

  - user: root
  - 公网ip: 123.123.123.123

- 本机

- ssh

  ```sh
  # 反向代理
  ssh -fCNR [B机器IP或省略]:[B机器端口]:[A机器的IP]:[A机器端口] [登陆B机器的用户名@服务器IP]
  # 正向代理
  ssh -fCNL [A机器IP或省略]:[A机器端口]:[B机器的IP]:[B机器端口] [登陆B机器的用户名@B机器的IP]
  # 参数
  -f 后台执行ssh指令
  -C 允许压缩数据
  -N 不执行远程指令
  -R 将远程主机(服务器)的某个端口转发到本地端指定机器的指定端口
  -L 将本地机(客户机)的某个端口转发到远端指定机器的指定端口
  -p 指定远程主机的端口
  
  ```

  

### 反向代理 （A）

```sh
ssh -fCNR [B机器IP或省略]:[B机器端口]:[A机器的IP]:[A机器端口] [登陆B机器的用户名@服务器IP]
# 代理
ssh -fCNR 7280:localhost:22 root@123.123.123.123
# 查看
ps aux | grep ssh
```

### 正向代理（B）

```sh
ssh -fCNL [A机器IP或省略]:[A机器端口]:[B机器的IP]:[B机器端口] [登陆B机器的用户名@B机器的IP]
# 代理
ssh -fCNL *:1234:localhost:7280 localhost
# 查看
ps aux | grep ssh
```

### 远程连接 A

```sh
ssh -p1234 inside@123.123.123.123 
```

### 稳定连接

#### 免密码登陆

1. 免去反向代理密码（A）

```sh
ssh-copy-id root@123.123.123.123
```

2. 免去正向代理密码（B）

```sh
ssh-copy-id root@localhost
```

#### autossh

使用autossh自动重连断开的隧道（A反向代理）

- ```sh
  autossh -M 7281 -fCNR 7280:localhost:22 root@123.123.123.123 
  ```

- 相比 `ssh` 多出一个参数 `-M 7281` 指定断开重连的沟通端口

- 增加启动自动运行

