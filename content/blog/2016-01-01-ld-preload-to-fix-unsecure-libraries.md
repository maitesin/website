+++
title = "LD_PRELOAD to fix unsecure libraries"
date = "2016-01-01T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Linux", "Security"]
categories = ["Operating Systems"]
+++

## Introduction

I have seen LD_PRELOAD used in several cases. From using it to *allow programs that link to a newer version of the 
libstdc++*, to *cracks for applications that hijack some calls and provide the expected result to tell the application they have a valid license*.

**The aim of this post is to show how to find these dangerous calls in applications that you are running which you cannot fix (i.e. you do not have access to the source code).** Imagine that one of these applications uses the library call *strcpy*, as we know that call is dangerous and we have more secure alternatives such as *strncpy*.

**All the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/ld_preload_2016_01_01/src)**

As an example of these applications I will use the following code:

``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[])
{
	if (argc <= 1)
	{
		printf("Bad number of parameters.\nUsage: %s <string up to 512 characters>\n", argv[0]);
		return 1;
	}
	char s[512];
	strcpy(s, argv[1]);
	printf("You introduced: %s\n", s);
	return 0;
}
```
An example of its execution is the following:

``` bash
$ ./app Wololo
You introduced: Wololo
```

As you can imagine, we will have problems if the user gives a string longer than 511 characters to the application because it will
override more than just the string. Actually, it can even be an entry point for an exploit (it depends on the compiling flags).

``` bash
$ ./app $(perl -e 'print "A"x1000')
You introduced: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[1] 6625 segmentation fault (core dumped) ./app $(perl -e 'print "A"x1000')
```

## Find which dangerous calls are happenning in the application

To help us in this task we will use **ltrace**. Remember, we do not have access to the code.

``` bash
$ ltrace ./app Wololo
__libc_start_main(0x4005f6, 2, 0x7ffc587856b8, 0x4006a0 <unfinished ...>
strcpy(0x7ffc587853c0, "Wololo")                                        = 0x7ffc587853c0
printf("You introduced: %s\n", "Wololo"You introduced: Wololo
)                                = 23
+++ exited (status 0) +++
```

In the output above we can see that the call *strcpy* is used. It is dangerous, so we want to use the call *strncpy* instead.

## Using a more secure call than *strcpy*

We can create our own version of the *strcpy* that actually calls *strncpy*:

``` c
#include<string.h>

char * strcpy(char * s1, const char * s2)
{
        strncpy(s1, s2, 511); //Copy up to the first 511 characters
        s1[511] = '\0'; // Set always the latest character to '\0'
        return s1;
}
```

Now we have to compile it as a shared object (library to link):

``` bash
gcc -shared -fPIC our_patch.c -o our_patch.so
```

## Using LD_PRELOAD to call our *strcpy*

LD_PRELOAD will be used to load out *strcpy* instead of the one provided by the standard library.

``` bash
$ LD_PRELOAD=$PWD/our_patch.so ./app $(perl -e 'print "A"x1000')
You introduced: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�@
```

Note that it only copies up to the first 511 characters of the string s2.

## Conclusion

I want to point out the versatility of the LD_PRELOAD, for example think about how can this help mitigate a 0-day exploit until the code is fixed.

This use of LD_PRELOAD is quite common in competitions like a [CTF](https://en.wikipedia.org/wiki/Capture_the_flag#Computer_security) (in the attach/defense style) where you are provided with a server (with some services running) and you have to keep alive your services as much time as you can, but usually the services are an older version with known issues you need to patch on the fly ;)
