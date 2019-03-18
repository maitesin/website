+++
title = "My two cents about Go"
date = "2015-06-24T13:50:46+02:00"
author = "Oscar Forner"
tags = [""]
categories = ["Development"]
+++

### Table of Contents
[TOC]

### Introduction
There is plenty of meterials such as talks, tutorials and posts talking about **Go**, but I want to give my opinion about what I think are the strenghts and weaknesses of **Go**.

**Full disclosure**: *I do not use **Go** at work. I use **Go** in my personal projects. Therefore, **take my opinions with a grain of salt.***

### Pros
**Go** is one of the best programming languages I have seen in my whole life. I think that because of the following characteristics.

#### Standard library
If you ever asked me "Which programming language has the best and more complete standard library?" before trying **Go** I would have answered **Python**. Nowadays, I would answer **Go** has the best and more complete standard library.

To back up my statement that **Go** has the best and more complete standard library:

* It has a library for **encoders** and a library for **decoders**. They contain encoders and decoders for formats such as **json**, **xml**, **csv**, **base64**, **hex**, etc.
* It has a **compress** library that contains the following formats **bzip2**, **flate**, **gzip**, **lzw** and **zlib**.
* It has a **crypto** library with algorithms such as **aes**, **dsa**, **md5**, **rc4**, **rsa**, **sha1**, **sha256**, **sha512**, etc.
* It has a **database** library that contains a generic interface for **SQL**. It does not contain specific drivers, but it defines a common interface for all of them. Therefore, changing the backend will be pretty simple.
* It has a **go** library that contains all the required dependencies in order to format, parse and build any valid **Go** source code. It contains modules such as **ast**, **build**, **doc**, **format**, **parser**, **token**, **types**, etc.
* It has an **image** library that can handle formats such as **gif**, **jpeg** and **png**.
* It has a **math** library that has a **big** module to handle arbitrary-precision arithmetic.
* It has a **net** library that contains modules such as **http**, **mail**, **smtp** and **url**.
* It has a library for **run-time reflexion** called **reflect**.
* It has a **testing** library to perform the **unit testing**.

Obviously that is no the only content of the standard library, but these were the packages that I found to be the more interesting.

#### Unit test and benchmarking
I really love the idea of the compiler of the language having the ability to run the **unit testing** and the **benchmarking** in such a simple way.

To run all the **unit test** you just have to do the following:
``` bash
go test
```

You can also run the **unit test** from a specific file with:
``` bash
go test file.go
```

To run all the **unit test** that match a provided pattern you can do the following:
``` bash
go test -run "Pattern*"
```

To perform the **benchmarking** of the unit test you have to do the following:
``` bash
go test -bench=.
```

Finally, you can limit the amount of time the **benchmark** is running:
``` bash
go test -bench=. -benchtime=20s
```

#### Channels
This is one of the big features of **Go**. If you ever used a **Unix** system, this feature will remind you of **pipes**. This is because a **channel** is used to send data between a reader and a writer (usually **Goroutines**).

There is plenty of good documentation about **channels** in [**Go** by Example](https://gobyexample.com/channels) and in [A Tour of **Go**](https://tour.golang.org/concurrency/2). So, there is no need for me to write examples. 

### Cons
Not everything is perfect in **Go**. There are some perks that once they are fixed will make **Go** an even better programming language.

#### Build system
One of the main flaws of **Go** is the lack of a standard **build system**. I can understand that older languages such as **C** or **C++** do not have a standard **build system**. Newer languages usually have a **build system**, not always from the beginning, such as **Python** or the more recent **Rust**.

Getting a standard **build system** for **Go** would be a great advantage. Maybe for **Go** 2.0.

#### Different versions of the compiler
This issue is not my biggest concern, but it is something that could be problematic for some people. The main problem is having to change the environment variables ***$GOROOT*** and ***$GOPATH***. In **Python**, I can choose to use **Python2** or **Python3** calling different executables. The same for **C** and **C++**, I can call different versions of the compiler because they can coexist in the filesystem.

### Other
In this section I talk about some features of **Go** that **are both a Pro and a Con**.

#### Runtime
Since I come from a systems programming background, I find hard to like a programming language that has a runtime. Unless such **programming language brings more to the table to compensate for the runtime**, I will try to avoid using it. 

**Go is one of the few languages that actually brings cool features in its runtime** like detection of concurrency problems such as **deadlocks**.

#### Generics
The lack of generics in the **Go** language may make some people doubt the usefulness of the language, however, I do not mind not having generics. It could be because I have not yet created a big project using **Go**, so I have not needed them.

Maybe in **Go** 2.0 they will introduce some feature to address this perk. Nevertheless, I am not confident using this argument against **Go**. I have used **C** for long time and I never felt the need for generics. Therefore, I can live with a language that does not have them.

#### Goroutines
This is another of the big features of **Go** and some **people will be surprised of it not being a Pro in this post**. Don't get me wrong, I think **Goroutines** are awesome, but you need the **runtime** to make them work.

That is because **Goroutines do not use the thread system provided by the operating system**. It uses its own implementation of thread. And all that dependency, locality, lifetime, etc. of the thread is handled by the runtime.

### Conclusion
I think **Go is already a great language**, even with the small **Cons** I talk about in this post. Once the people in charge of the language fix this perks, **Go** will become an even better language. **Go** is a mature language with an awesome **standard library** and great tools. **I will not be surprised if Go starts replacing Python in some niches even before Go gets a standard build system.**
