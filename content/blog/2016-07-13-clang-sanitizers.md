+++
title = "Clang sanitizers"
date = "2016-07-13T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Clang", "C", "C++"]
categories = ["Development"]
+++

## Introduction

**[Clang](http://clang.llvm.org/)** is a compiler front end for the C, C++, Objective-C and Objective-C++ programming languages. It uses [LLVM](http://llvm.org/) as its back end. In this post I talk about some of the **sanitizers** available in **Clang** (some are avilable in **GCC** as well). **They help you detect problems at run time (dynamic analysis).**

As usual, I am working from an Arch Linux computer. Therefore, I can install **Clang** and the tools from the repository (clang). For other distributions you can find the information in the documentation.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/clang_sanitizers_2016_07_13)**.

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

## Clang sanitizers

The **Clang** sanitizers available are:

* **AddressSanitizer**: detects memory errors. [http://clang.llvm.org/docs/AddressSanitizer.html](http://clang.llvm.org/docs/AddressSanitizer.html)
* **ThreadSanitizer**: detects data races. [http://clang.llvm.org/docs/ThreadSanitizer.html](http://clang.llvm.org/docs/ThreadSanitizer.html)
* **MemorySanitizer**: detects uninitialized reads. [http://clang.llvm.org/docs/MemorySanitizer.html](http://clang.llvm.org/docs/MemorySanitizer.html)
* **UndefinedBehaviorSanitizer**: detects undefined behavior. [http://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html](http://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
* **DataFlowSanitizer**: is a generalised dynamic data flow analysis. Unlike other **sanitizers** this one is not designed to detect a specific class of bugs on its own, it provides a generic dynamic data flow analysis framework to be used by clients to help detect application-specific issues within their own code. [http://clang.llvm.org/docs/DataFlowSanitizer.html](http://clang.llvm.org/docs/DataFlowSanitizer.html)
* **LeakSanitizer**: detects memory leaks. It can be combined with **AddressSanitizer**. [http://clang.llvm.org/docs/LeakSanitizer.html](http://clang.llvm.org/docs/LeakSanitizer.html)

In this post I show **AddressSanitizer**, **ThreadSanitizer**, **MemorySanitizer** and **UndefinedBehaviorSanitizer**. I do not talk about **DataFlowSanitizer** because it is a work in progress and it is really specific of the application where you need it. Moreover, I do not talk about **LeakSanitizzer** because it is a subset of checks from **AddressSanitizer** that can be run independently from it.

## AddressSanitizer

### Usage of freed memory

The code below is trying to use a region of memory that has been freed already.

``` cpp
int main()
{
  int *array = new int[100];
  delete [] array;
  return array[1];
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=address -g -o free free.cpp
```

When you run the previously generated executable you will get something similar to the following:

{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/3zcpyg71hz6sxnhhxru7pvgtj.js" id="asciicast-3zcpyg71hz6sxnhhxru7pvgtj" async></script>
{{< /rawhtml >}}

### Buffer overflow

The code below is trying to access a memory region that is not part of the allocated one.

``` cpp
int main()
{
  int * array = new int[50];
  return array[100];
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=address -g -o overflow overflow.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/c0338bklzn84ptgafgaj4kas3.js" id="asciicast-c0338bklzn84ptgafgaj4kas3" async></script>
{{< /rawhtml >}}

### Memory leak

The code below is allocating memory twice but it only frees the memory once.

``` cpp
int main()
{
  int * array = new int[5];
  array = new int[10];
  delete [] array;
  return 0;
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=address -g -o leak leak.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/91kmpmy03843ccdbbh04ptbdd.js" id="asciicast-91kmpmy03843ccdbbh04ptbdd" async></script>
{{< /rawhtml >}}

### Double free

The code below is allocating memory once but it is freeing it twice.

``` cpp
int main()
{
  int * array = new int[5];
  delete [] array;
  delete [] array;
  return 0;
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=address -g -o double_free double_free.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/ebgp9ox48e8ffdaf0iug0b37s.js" id="asciicast-ebgp9ox48e8ffdaf0iug0b37s" async></script>
{{< /rawhtml >}}

## ThreadSanitizer

### Data race

The code below has a data race due to having two threads modifying the same global variable.

``` cpp
#include <iostream>
#include <pthread.h>

int GLOBAL;

void * SetGlobalTo2(void * x) {
  GLOBAL = 2;
  return x;
}

void * SetGlobalTo3(void * x) {
  GLOBAL = 3;
  return x;
}

int main()
{
  pthread_t thread1, thread2;
  pthread_create(&thread1, NULL, SetGlobalTo2, NULL);
  pthread_create(&thread2, NULL, SetGlobalTo3, NULL);
  pthread_join(thread1, NULL);
  pthread_join(thread2, NULL);
  std::cout << GLOBAL << std::endl;
  return 0;
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=thread -g -lpthread -o race race.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/5go47caz8s1t6mdsaexb10ecx.js" id="asciicast-5go47caz8s1t6mdsaexb10ecx" async></script>
{{< /rawhtml >}}

## MemorySanitizer

### Uninitialized values

The code below is reading the value stored in an array that has not been initialized.

``` cpp
int main()
{
  int *array = new int[50];
  return array[42];
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=memory -g -o memory memory.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/enrqyt3iue9lvmixapugzljge.js" id="asciicast-enrqyt3iue9lvmixapugzljge" async></script>
{{< /rawhtml >}}

## UndefinedBehaviorSanitizer

### Function not returning a value

The code below contains a function that must return an integer, but it does not.

``` cpp
int must_return_value()
{
  int result = 0;
  result += 1;
}

int main()
{
  int value = must_return_value();
  return value;
}
```

We can compile it with:

``` bash
clang++-3.8 -fsanitize=undefined -g -o function function.cpp
```

When you run the previously generated executable you will get something similar to the following:
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/bqcprr20fga4yrdyq69vs3aek.js" id="asciicast-bqcprr20fga4yrdyq69vs3aek" async></script>
{{< /rawhtml >}}


## Conclusion

Using these tools to compile your code **to run your tests (integration test, smoke test, system test, etc) helps you catch plenty of problems**. The downside is that you **cannot use two sanitizers at the same time** (except **AddressSanitizer** and **LeakSanitizer**). Therefore, you need multiple binaries to test your code with all these sanitizers, but the payoff is worth it.
