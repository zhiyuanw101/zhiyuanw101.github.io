---
layout: post
title: Git 进阶
categories: [Git, Utils]
description: Git一些进阶，来自于使用经验与官方文档
keywords: Utils, Git
---

## 使用分支 [cite]((https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6))


### 1. 基本流程

- 建立新本地分支

```bash
git clone <remote git>  
#clone仓库
git branch -b <dev>  
#创建分支
git checkout <dev>  
#切换分支
```

- 建立新的远程分支
  
```bash
git push origin <dev>  
#提交本地当前分支到远程dev分支
git push origin <dev>:<dev>  
#提交本地dev到远程dev分支
```

- 合并分支
  
```bash
git checkout master
#切换到master分支
git merge dev
```

- 提交远程master

```bash
git push origin master
```

- 删除本地分支
  
```bash
git branch -d <temp>
```

### 2. 基本操作

```bash
git diff <branch1> <branch2> #两branch区别
git branch          #查看本地branch
git brahch -a       #查看全部branch
git branch -r       #查看远程branch
git branch -v       #查看每个分支最后一次提交
git push origin :<dev> #删除远程branch dev
```

### 3. 一些关键问题

- 切换分支：当你切换分支的时候，Git 会重置你的工作目录，使其看起来像回到了你在那个分支上最后一次提交的样子。 Git 会自动添加、删除、修改文件以确保此时你的工作目录和这个分支最后一次提交时的样子一模一样。
- 出现冲突：出现冲突的文件出现如下标记，手动选择其中一个修复

```bash
<<<<<<< HEAD:index.html
<div id="footer">contact : email.support@github.com</div>
=======
<div id="footer">
please contact us at support@github.com
</div>
>>>>>>> iss53:index.html
```  

- 远程分支/远程跟踪分支：
  - 远程分支位于服器上
  - 远程跟踪分支 `<remote>/<branch>` 是无法移动的本地引用
  - 两者不会自动同步，通过 `git fetch <branch>` 拉取对应远程分支的远程跟踪分支，`git fetch --all` 拉取全部，拉取不会修改工作区
  - 通过 `git merge <remote>/<branch>` 合并远程跟踪分支到当前
  - `git pull = git fetch + git merge`
- 跟踪分支：

    ```bash
    git checkout -b dev1 origin/dev1
    #从远程跟踪分支origin/dev1建立新分支dev1
    git checkout --track origin/dev1
    #快捷：
    git checkout dev1
    #快捷：本地dev1不存在，且有远程dev1
    ```
