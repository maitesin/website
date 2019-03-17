+++
title = "Unit test with Google Test for C++"
date = "2015-06-24T13:50:46+02:00"
author = "Oscar Forner"
tags = [""]
categories = ["Development"]
+++

![NAS Picture](https://oscarforner.com/static/img/nas/inside.jpg)

### Table of Contents
[TOC]

### Introduction

A **Network Attached Storage (NAS)** is a network appliance that contains one or more hard drives.

There are several things to take into account before building a **NAS**. For example, if you are going to build a **NAS** using parts from old computers or if you want to build a **NAS** with brand new parts. Another option is to buy an off the shelf **NAS**, but none of them, as far as I know, was using **ZFS** as their filesystem.

### Building a NAS

There is plenty of documentation, guides and tutorials about how to build a **NAS**. In my case I followed this guide [DIY NAS: 2016 Edition](https://blog.brianmoses.net/2016/02/diy-nas-2016-edition.html). The author of the blog has more recent builds, but the hardware he used in this one was closer to what I wanted.

The hardware I used for my **NAS** is the following:

 - Motherboard + CPU: ASRock C2750D4
 - RAM: Kingston 32GB (4x8GB) DDR3 ECC
 - PSU: EVGA SuperNOVA 650W 80+ Gold
 - HDD: 8 x Western Digital Red 3TB
 - Flash Drive: USB Sandisk 8GB
 - Case: Fractal Design - Define R5

The software I used for my **NAS** is [**FreeNAS**](http://www.freenas.org/). It is based on **FreeBSD** and it provides a simple but powerful UI. Another great characteristic is its native support for the [**ZFS** filesystem](https://en.wikipedia.org/wiki/ZFS).

In this case I am using **ZFS** with *raidz2*. That means **2 HDD can fail at the same time and the system will still be able to recover**.

#### Buying the hardware

In order **to avoid a bad batch of HDD I ordered all 8 hard drives at different times during the year and from different dealers**. All other parts were purcheased at the same time.

The reason to avoid a bad batch of HDD is because if more than 2 HDDs fail in my configuration, I would lose all the data stored in it.

#### Testing the hardware

I **always do some testing on the hardware** that I buy. In this case, the testing was harder because I wanted to make sure that everything was in good state before storing real data in it.

**The main two things I focused on the testing were the RAM and the HDDs**. I could have tested other parts such as the CPU or the Motherboard, but they are not as relevant for the data integrity.

**The RAM testing was just running [memtest](http://www.memtest.org/)**. After running for 24 hours and doing more than 2 passes without errors I thought it was good enough.

The HDDs testing involved performing writes of zeros into the drives for 36 hours and then writes of random data for another 36 hours. **The health of the HDDs was checked using [S.M.A.R.T.](https://en.wikipedia.org/wiki/S.M.A.R.T.)**.

The result of the test was that **both the RAM and the HDDs were in perfect working order.**

### Final thoughts

I have been using the **NAS** for about 2 months. I have to say that I am certainly impressed with the quality and stability of the **FreeNAS** software and the resilience of the **ZFS** filesystem, I strongly recommend both. **FreeNAS** had two updates since I installed it, both of them went fine and there was no need for me to do anything else besides giving it permission to install them.
