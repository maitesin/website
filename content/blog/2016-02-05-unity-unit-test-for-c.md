+++
title = "Unity: unit test for C"
date = "2016-02-05T13:50:46+02:00"
author = "Oscar Forner"
tags = ["C", "Unity", "Unit Test"]
categories = ["Development"]
+++

**Unity** is one of the available frameworks to create **unit tests** for C. In this example, I will use **CMake** to configure the project and build.

**All the code and configuration files used in this post are available in this
[repo](https://github.com/maitesin/blog/tree/master/unity_c_unit_test_2016_02_05) in GitHub.**

### Can you do unit test in C? And what is Unity?

**Some people do not know you can do unit tests in C** and people must do **unit tests** in any language. My choice to do **unit tests** in C is **Unity** for several reasons:

 * No need to install any package in your distro. Just add the three files to your project and start using it.
 * Great documentation and examples in the [repo](https://github.com/ThrowTheSwitch/Unity) and their [website](http://www.throwtheswitch.org/).
 * Awesome course about **unit test** in **embedded systems** on [Udemy](https://www.udemy.com/unit-testing-and-other-embedded-software-catalysts/). I did it myself, totally worth it if you are interested in these topics.

### Structure of the project

In the root of the project we have the **CMakeLists.txt** file and three folders: *lib*, *src* and *unittest*.

 * *lib*: Contains the **Unity** files.
 * *src*: Contains the code we want to test. In this case, a functions header file.
 * *unittest*: Contains the test we want to run.

``` bash
$ ls -R
.:
CMakeLists.txt  lib  src  unittest

./lib:
unity.c  unity.h  unity_internals.h

./src:
functions.h

./unittest:
test_functions.c
```

### The project to test

The configuration will be done in the **CMakeLists.txt** file:

``` cmake
project(Unity_example)
cmake_minimum_required(VERSION 2.8)

INCLUDE_DIRECTORIES(src)
INCLUDE_DIRECTORIES(lib)
ADD_EXECUTABLE(run_test unittest/test_functions.c lib/unity.c)
```

The code we want to test is:

``` c
int sum(int a, int b)
{
        return a + b;
}
```

Finally, the **unit test**:

``` c
#include "functions.h"
#include "unity.h"

void test_two_plus_two(void)
{
        TEST_ASSERT_EQUAL_INT(4, sum(2, 2));
}

void test_minus_two_plus_two(void)
{
        TEST_ASSERT_EQUAL_INT(0, sum(-2, 2));
}

int main(void)
{
        UNITY_BEGIN();
        RUN_TEST(test_two_plus_two);
        RUN_TEST(test_minus_two_plus_two);
        return UNITY_END();
}
```

As you can see in the code above, you need a main in the **unit test** file that contains: *UNITY_BEGIN* and *UNITY_END* calls and a *RUN_TEST* call for each test we want to run.

### Conclusion

**Everybody should be doing unit tests, it does not matter what language do they use**. I do use this framework among others (that I will introduce in future posts) for testing C applications. **Unity** is a must have tool for any C developer, **even for embedded software**. You can check it in their website and course.
