---
layout: post
title: Linux 进阶
categories: [Linux, Utils, OS]
description: Linux 进阶
keywords: Linux, Utils, OS
---

## shell script

### [Linux Permissions](https://www.guru99.com/file-permissions.html)

add execute permission:

```sh
chmod +x file
```

### script [Shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))

```sh
#!/bin/bash
```

### [Stop on errors](https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/)

```sh
set -Eeuo pipefail
```