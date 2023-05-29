+++
title = "Cling a C++ interpreter"
date = "2016-01-08T13:50:46+02:00"
author = "Oscar Forner"
tags = ["C++", "Clang", "Interpreter"]
categories = ["Development"]
+++

## Introduction

**Cling is an interactive C++ interpreter**, built on top of Clang and LLVM compiler infrastructure. It can be found in
[GitHub](https://github.com/vgvassilev/cling) (Note: Lately there has not been that much development on it).

Since I use Arch Linux I am lucky to have cling in the AUR repository (cling-git). For other ones you can use the
[cling-all-in-one](https://github.com/karies/cling-all-in-one/) repo that contains a script to download all dependencies, compile and build cling for you.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/cling_interpreter_2016_01_08/src)**

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

## The basics of Cling

In this section I will show the basic commands we can run on cling besides C/C++ code.

| Command | Explanation |
|---|---|
| .I *path* | to add includes. Like -I option at compiling time |
| .L *file* | to load file. This is important to try classes or functions that you already have |
| .rawInput | Toggle wrapping and printing the execution results of the input |
| .help | Shows a nice help with these and other commands that can be used |

## Examples of usage

In this section examples of usage using the basics from the previous section will be shown.

### Load an existing file with a function we want to test

In this first example the following header will be loaded to use it:

``` c
//Extremely useful function
bool is_greater(int a, int b) {
        return a > b;
}
```

The header above can be used from Cling as shown in the following video:
<script type="text/javascript" src="https://asciinema.org/a/0tlo8e6kltl1lvqcrm8vz6pxr.js"
id="asciicast-0tlo8e6kltl1lvqcrm8vz6pxr" async></script>

### Include a folder and load a template class from that folder

This example will include a folder that contains a class that will be loaded from Cling:

``` cpp
template <typename T>
class MyClass {
public:
        MyClass(const T & t) : total(t) {}
        T inc();
        T dec();
private:
        T total;
};
```

``` cpp
#include "my_class.h"

template <typename T>
T MyClass<T>::inc() {
        return ++total;
}

template <typename T>
T MyClass<T>::dec() {
        return --total;
}
```

The class above can be loaded from Cling as shown in the following video:
<script type="text/javascript" src="https://asciinema.org/a/6dn649p755qhet4dr854vsclz.js"
id="asciicast-6dn649p755qhet4dr854vsclz" async></script>

### Write a function on-the-fly

Cling allows us to write functions or classes on-the-fly:
<script type="text/javascript" src="https://asciinema.org/a/82i6wmeyjiyd2j6ohlhum0zm9.js"
id="asciicast-82i6wmeyjiyd2j6ohlhum0zm9" async></script>

## Conclusion

I do not consider Cling as my main way to work in C/C++, but **it is my first option when I want to try something quick
in a function or a class** that I am interested in using. It is not a perfect tool for everything, but it is faster than setting
up a whole example when you are only interested in something specific.
