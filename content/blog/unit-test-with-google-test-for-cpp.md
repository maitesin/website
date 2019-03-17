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
**Google Test** is one of the available Frameworks to create **unit test** for C++. In this example I will use **CMake**
to configure the project and build. Furthermore, for the **dependency manager** I will use the new and shiny
**[conan](https://www.conan.io/)**.

Before starting, why use a **dependency manager** such as conan or software to configure and build such as **CMake**?
Because these technologies are widely use it in real projects.

**All the code and configuration files used in this post are available in this
[repo](https://github.com/maitesin/blog/tree/master/google_test_2015_12_22) in GitHub.**

### Step 1 Install conan, configure project and gather dependencies
First of all we need to have install conan from pip2 doing:
``` bash
pip2 install conan
```

Now with conan installed we do not have to worry about installing **Google Test** in our system.

Next step will be preparing the **conanfile.txt** to gather de dependencies:
``` bash
[requires]
gtest/1.7.0@lasote/stable

[options]
gtest:shared=True

[generators]
cmake
```

Once we have conan ready we only need to run it to download the dependency and configure them to have them ready for
CMake:
``` bash
conan install .
```
This will output something similar to:
``` bash
WARN: Migration: Updating settings.yml with new gcc versions
Requirements
    gtest/1.7.0@lasote/stable
    Package for gtest/1.7.0@lasote/stable in
    /home/maitesin/.conan/data/gtest/1.7.0/lasote/stable/package/ca89189bc59ff53842d6beea76549f289b7b88bd
    Generated conaninfo.txt
Generated conanbuildinfo.cmake
```

### Step 2 configuring CMake
The configuration will be done in the **CMakeLists.txt** file:
``` cmake
project(Google_test_example)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

INCLUDE_DIRECTORIES(src)
ADD_EXECUTABLE(run_test src/test.cpp)
TARGET_LINK_LIBRARIES(run_test ${CONAN_LIBS})
```

### Step 3 code and unit test
The code will be held in the **src** folder. It will contain two files: *functions.h* and *test.cpp*.

The function(s) we want to test will be in the header file *function.h*:
``` c
int int_addition(int a, int b) {
            int c = a + b;
            return c;
}
```


The test(s) we want to run will be in the source file *test.cpp*:
``` cpp
#include "gtest/gtest.h"
#include "functions.h"

TEST(IntAddition, Negative) {
            EXPECT_EQ(-5, int_addition(-2, -3)) << "This will be shown in case it fails";
            EXPECT_EQ(-3, int_addition(5, -8));
}

TEST(IntAddition, Positive) {
            EXPECT_EQ(4, int_addition(1, 3));
            EXPECT_EQ(9, int_addition(4, 5));
}

int main(int argc, char **argv) {
            testing::InitGoogleTest(&argc, argv);
            return RUN_ALL_TESTS();
}
```

### Step 4 putting all together
What is left to do is actually build the project and run the test. In order to do this we need to run:
``` bash
cmake .
```

This will output something similar to:
``` bash
-- The C compiler identification is GNU 5.3.0
-- The CXX compiler identification is GNU 5.3.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/maitesin/workspace/blog/google_test_2015_12_22
```

There will be now a **Makefile** generated from **CMake** with everything ready to compile and link all the sources and
dependencies together.
``` bash
make
```

This will output something like:
``` bash
Scanning dependencies of target run_test
[ 50%] Building CXX object CMakeFiles/run_test.dir/src/test.cpp.o
[100%] Linking CXX executable bin/run_test
[100%] Built target run_test
```

This will generate an executable in the *bin* folder, and we will be able to run them with the command:
``` bash
./bin/run_test
```

This will result with the following output:
``` bash
[==========] Running 2 tests from 1 test case.
[----------] Global test environment set-up.
[----------] 2 tests from IntAddition
[ RUN      ] IntAddition.Negative
[       OK ] IntAddition.Negative (0 ms)
[ RUN      ] IntAddition.Positive
[       OK ] IntAddition.Positive (0 ms)
[----------] 2 tests from IntAddition (0 ms total)

[----------] Global test environment tear-down
[==========] 2 tests from 1 test case ran. (0 ms total)
[ PASSED ] 2 tests.
```

### More advanced example
These are the basics of how to use **Google Test** to create **unit test** for your application. In the website of the project there are plenty of more advanced examples.

Finally, if you want to see how is used **Google Test** in one of my own project you can have a look to the repository [tries](https://github.com/maitesin/tries). For each of the three data structures (Trie, TST and Radix Tree) there are two folders: **lib** (where the source code of the data structure is stored) and **gtest** (where the unit test are stored).
