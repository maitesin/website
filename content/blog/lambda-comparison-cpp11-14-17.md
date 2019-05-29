+++
title = "Lambda comparison C++11/14/17"
date = "2016-05-14T13:50:46+02:00"
author = "Oscar Forner"
tags = ["C++", "C++11", "C++14", "C++17", "Lambda"]
categories = ["Development"]
+++

### Introduction

In this post I talk about what has been added in the **C++ standard** regarding **lambda expressions** since they were introduced in **C++11**.

**All the code and configuration files used in this post are available in this
[repo](https://github.com/maitesin/blog/tree/master/lambda_comparison_2016_05_14) in GitHub.**

### What is a lambda expression?

A **lambda expression** is a simplified notation for defining and using an anonymous function object. Instead of defining a named class with an *operator()*, later making an object of that class and finally invoking it.[^1]

I do not explain all the options for capturing or specifying return types. There is plenty of material regarding these topics. I focus on what has been introduced in **C++14** and what will be introduced in **C++17**.

### Basics of the lambda expression

The following is the smallest **lambda expression** with its three parts:

- **[]**: capture.
- **()**: parameters.
- **{}**: body.

``` cpp
[](){}
```

The following **lambda expression** increments by one the parameter.

``` cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
  std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  auto my_lambda = [](int x) { return x + 1; };
  std::transform(v.begin(), v.end(), v.begin(), my_lambda);
  for (auto &value : v) {
    std::cout << value << std::endl;
  }
  return 0;
}
```

The result of the execution of the previous code is:

``` bash
2
3
4
5
6
7
8
9
10
11
```

The following **lambda expression** shows the difference between capturing by value **=** and by reference **&**:

``` cpp
#include <iostream>

int main() {
  int i = 1;
  auto copy = [=](){ std::cout << i << std::endl; };
  auto ref = [&](){ std::cout << i << std::endl; };
  copy();
  ref();
  ++i;
  copy();
  ref();
  return 0;
}
```

The result of the execution of the previous code is:

``` bash
1
1
1
2
```

### What has been added in C++14

In **C++14** two new features were added to **lambda expressions**:

- **Initialization captures**: A capture with an initializer acts as if it declares and explicitly captures a variable declared with type auto, whose declarative region is the body of the **lambda expression**.[^2]
- **Generic lambda expressions**: Until **C++14** parameters of a **lambda expression** should be of a specific type. Now, **lambda expressions** accept **auto** as a valid parameter type.

Example of the **initialization captures**:

``` cpp
#include <iostream>

int main() {
  int x = 1;
  auto my_lambda = [&z = x]() { z += 1; };
  my_lambda();
  std::cout << x << std::endl;
  return 0;
}
```

The result of the execution of the previous code is:

``` bash
2
```

Example of a **generic lambda expression**:

``` cpp
#include <iostream>

int main() {
  auto my_lambda = [](auto &a, auto &b) { return a < b; };
  float af = 1.5, bf = 2.0;
  int ai = 3, bi = 1;
  std::cout << "Float: " << my_lambda(af, bf) << std::endl;
  std::cout << "Integer: " << my_lambda(ai, bi) << std::endl;
  return 0;
}
```

The result of the execution of the previous code is:

``` bash
Float: 1
Integer: 0
```

### What will be added in C++17

The current plan is to add two new features for **lambda expressions** in **C++17**:

- **Capture &lowast;this**: This will allow the **lambda expression** to capture the **enclosing object by copy**. This will make possible to use safely the **lambda expression** even after the **enclosing object** has been destroyed.
- **constexpr lambda expressions**: This will allow to call **lambda expressions** and use their result to generate ***constexpr*** objects **at compile time**.

Sadly neither [GCC](https://gcc.gnu.org/projects/cxx-status.html#cxx1z) or [Clang](http://clang.llvm.org/cxx_status.html) in any stable version supports them. Therefore, **there will not be any execution of code, but there is some code that should work once the features are implemented**. The information used to do the code of this section has been found in the [C++ reference website](http://en.cppreference.com/w/cpp/language/lambda) and in [the paper for constexpr lambda expressions](https://isocpp.org/files/papers/N4487.pdf).

The following is an example of the **capture &lowast;this**:

``` cpp
struct my_struct {
  int x;
  void value();
};

void my_struct::value() {
  [=, *this](){};
}
```

The following is an example of the **constexpr lambda expression**:

``` cpp
#include <iostream>

int main() {
  constexpr auto multi = [](int a, int b){ return a * b; };
  static_assert(multi(3,7) == 21, "3x7 == 21");
  static_assert(multi(4,5) == 15, "4x5 != 15");
  return 0;
}
```

**Note**: Once **GCC** or **Clang** support these features I will try the code above and I will ammend it if necessary.

[^1]: Definition extracted from the book **The C++ Programming Language (Fourth Edition)**.
[^2]: Definition extracted from the website [cppreference.com](http://en.cppreference.com/w/cpp/language/lambda).
