---
layout: post
title: Git 进阶
categories: [Git, Utils]
description: Git一些进阶，来自于使用经验与官方文档
keywords: Utils, Git
---

# Git 进阶
## [使用分支](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6)
1. 基本流程
    - 建立新本地分支
    ```bash
    git clone [remote git]    
    #clone仓库
    git branch -b [dev]  
    #创建分支
    git checkout [dev] 
    #切换分支
    ```
    - 建立新的远程分支
    ```bash
    git push origin [dev]       
    #提交本地当前分支到远程dev分支
    git push origin [dev]:[dev] 
    #提交本地dev到远程dev分支
    ```
    - 合并分支
    ```bash
    git checkout master
    #切换到master分支
    git merge dev
    ```
    - 提交远程master
    ```
    git push origin master
    ```
    - 删除本地分支
    ```bash
    git branch -d [temp]
    ```
2. 基本操作
```bash
git diff [branch1] [branch2] #两branch区别
git branch          #查看本地branch
git brahch -a       #查看全部branch
git branch -r       #查看远程branch
git push origin :[dev] #删除远程branch dev
```
3. 详细
- 切换分支：当你切换分支的时候，Git 会重置你的工作目录，使其看起来像回到了你在那个分支上最后一次提交的样子。 Git 会自动添加、删除、修改文件以确保此时你的工作目录和这个分支最后一次提交时的样子一模一样。