---
layout: post
title: SSH Forwarding
categories: [Wiki, SSH, Utils]
description: Wiki
keywords: SSH Forwarding
---
[Link](https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot)

## Local Forwarding

Used when trying to connect to Target, access Target by accessing `LocalIP:LocalPort` connected to Server.
Local port, forward remotely.

```sh
ssh -L [LocalIP:]LocalPort:TargetIP:TargetPort User@Server
```

- means connect with ssh to `User@Server`, all connection attempts to `LocalIP:LocalPort` (client) to be forwarded `TargetIP:TargetPort` on the remote side.
- requires `User@Server` connected with `TargetIP`
- `TargetIP` is relative to `User@Server`, if they are on the same machine, `TargetIP` could be `localhost`
- Also can be configured in `.ssh/config`:
  
  ```sh
  # 9999 as LocalPort
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

Used when allowing others to connect to Target (connected with local), others access Target by accessing `RemoteIP:RemotePort` on Server.
Remote port, forward locally. 

```sh
ssh -R [RemoteIP:]RemotePort:TargetIP:TargetPort User@Server
```

- meaning connect ssh with `User@Server`, all connections to `RemoteIP:RemotePort` to be forwarded to `TargetIP:TargetPort` on the local side.
- `TargetIP:TargetPort` relative to local machine that set up the ssh

![SSH-R](/assets/images/SSH-R.png)