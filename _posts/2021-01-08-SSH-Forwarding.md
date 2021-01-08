---
layout: post
title: SSH Forwarding
categories: [Wiki, SSH, Utils]
description: Wiki
keywords: SSH Forwarding
---

## Local Forwarding

Used when trying to connect to Target, access Target by accessing `SourceIP:SourcePort` connected to Server

```sh
ssh -L [SourceIP:]SourcePort:TargetIP:TargetPort User@Server
```

- means connect with ssh to `User@Server`, forward all connection attempts to `SourceIP:SourcePort` to `TargetIP:TargetPort`
- requires `User@Server` connected with `TargetIP`
- `TargetIP` is relative to `User@Server`, if they are on the same machine, `TargetIP` could be `localhost`
- Also can be configured in `.ssh/config`:
  
  ```sh
  # 9999 as SourcePort
  # localhost:8888 as TargetIP:TargetPort
  # vm as User@Server
  Host vm
    User username
    HostName host_ip
    IdentityFile ~/.ssh/id_rsa
    LocalForward 9999 localhost:8888
  ```

![SSH_L](/assets/images/SSH-L.png)
![SSH-L1](/assets/images/SSH-L1.PNG)

## Remote Forwarding

Used when allowing others to connect to Target (connected with local), others access Target by accessing RemoteIP:RemotePort on Server

```sh
ssh -R [RemoteIP:]RemotePort:TargetIP:TargetPort User@Server
```

- meaning connect ssh with `User@Server`, Forward all connections to `RemoteIP:RemotePort` to `TargetIP:TargetPort`, which is connected to your local machine.
- `TargetIP:TargetPort` relative to local machine that set up the ssh

![SSH-R](/assets/images/SSH-R.png)