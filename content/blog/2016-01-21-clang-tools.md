+++
title = "Clang tools"
date = "2016-01-21T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Clang", "C", "C++"]
categories = ["Development"]
+++

## Introduction

**[Clang](http://clang.llvm.org/)** is a compiler front end for the C, C++, Objective-C and Objective-C++ programming languages. It uses [LLVM](http://llvm.org/) as its back end. There are also several awesome tools build on top of **Clang** and I am going to show the three of them I use the most.

As usual, I am working from an Arch Linux computer. Therefore, I can install **Clang** and the tools from the repository (clang, clang-tools-extra). For other distributions you can find the information in the documentation.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/clang_tools_2016_01_29)**.

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

## Clang-format

This tool is **perfect to make sure that you are following a specific code style** and it is fully configurable.

It can integrated in your editor or IDE. In my case, I have it integrated in my Vim configuration. You can see how it works in the following video:
<script type="text/javascript" src="https://asciinema.org/a/eas94n9bjs27c35xuix875xum.js" id="asciicast-eas94n9bjs27c35xuix875xum" async></script>

Or it can be used from the command line. The original state of the code is:

``` cpp
#include <iostream>
#include <vector>

int main(void) {
        std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
                std::cout << *it << std::endl;}
return 0;
}
```

After formatting:

``` cpp
#include <iostream>
#include <vector>

int main(void) {
  std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << std::endl;
  }
  return 0;
}
```

## Clang-tidy

This tool is really useful to have it integrated with your **version control system**. I like to have it configurated **to run as a pre-commit hook**. In case it detects any problem the commit fails. Therefore, you only commit code that has been aproved by the tool. As I use **CMake** I have to add a definition to generate the json file needed from the tool.

``` bash
cmake . -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

After that the code can be analyzed for all checks as follows:

``` bash
$ clang-tidy -checks='*' src/tidy.cpp 
1811 warnings generated.
/home/maitesin/workspace/blog/clang_tools_2016_01_29/tidy_example/src/tidy.cpp:5:16: warning: redundant boolean literal supplied to boolean operator [readability-simplify-boolean-expr]
        if (isGood == true) {
                      ^
            isGood
Suppressed 1810 warnings (1810 in non-user code).
Use -header-filter='.*' to display errors from all non-system headers.
```

You can deal on your own with these problems, or let it fix them for you using the *-fix* flag.
<script type="text/javascript" src="https://asciinema.org/a/def6c40kpd94p12i6e207gd4m.js" id="asciicast-def6c40kpd94p12i6e207gd4m" async></script>

## Clang-modernize

Last but not least, this tool is made **to update old code to C++11**. This tool is not bullet proof, but it can make your job easier if you have to migrate the old code to newer standards. It has an option called *-risk* that can have three values: *safe, reasonable or risky*, by default it uses *reasonable*.

Old code:

``` cpp
#include <iostream>
#include <vector>

int main(void) {
        int hardcoded[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        std::vector<int> v (hardcoded, hardcoded + sizeof(hardcoded) /
                            sizeof(int));
        for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
                std::cout << *it << std::endl;
        }
        return 0;
}
```

Modern code:

``` cpp
#include <iostream>
#include <vector>

int main(void) {
        int hardcoded[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        std::vector<int> v (hardcoded, hardcoded + sizeof(hardcoded) /
                            sizeof(int));
        for (auto & elem : v) {
                std::cout << elem << std::endl;
        }
        return 0;
}
```

## Conclusion

**These three tools make your live easier as a developer**. You will be sure you code is following the code style from your company/project, it will ensure that you are committing code that is using the new features from **C++11** and it will help you migrate the old code to use the features from **C++11**. I strongly recommend to include them in your workflow, because it will boost your work performance.

**NOTE: This post is based on **Clang** version 3.7.1. In version 3.8, clang-tidy will include some checks from clang-modernize. So, it will enforce you to use features from C++11**.
