+++
title = "Unit test with Google Test for C++"
date = "2015-06-24T13:50:46+02:00"
author = "Oscar Forner"
tags = [""]
categories = ["Development"]
+++

### Table of Contents
[TOC]

### Introduction
**As we all know the process of looking for a job is hard. And you have to stand out from the crowd**. Therefore, when I saw [s0ulshake's CV](https://github.com/soulshake/cv.soulshake.net) I wanted to do something similar, but with other technologies (you know I do not know JavaScript) and add the ability to move forward and backward.

I decided to code it in **Rust** because I have been looking for an excuse to start using it and this was as good as any other excuse :D. The way to distribute the binary is using **Docker**.

#### How to run my CV application

In order to run my CV application you just have to run
``` bash
sudo docker run -it maitesin/resume
```
and you will get something similar to:

![rust-cv](https://raw.githubusercontent.com/maitesin/rust-cv/master/cv.gif)

**For more information about the project please visit [https://oscarforner.com/projects/resume](https://oscarforner.com/projects/resume)**.
