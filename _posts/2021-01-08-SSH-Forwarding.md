---
layout: post
title: SSH Forwarding
categories: [Wiki, SSH, Utils]
description: Wiki
keywords: SSH Forwarding
---

## Local Forwarding

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

