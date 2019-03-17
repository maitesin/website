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
This post is a continuation from a previous post called [Unity; unit test for C](http://maitesin.github.io//Unity_unit_test_for_C/), but in this post we are going to use **FFF**.

**FFF** is one of the available mocking frameworks for C. In this example I will use **CMake** to configure the project and build it.

**All the code and configuration files used in this post are available in this [repo](https://github.com/maitesin/blog/tree/master/fff_mock_2016_02_18) in GitHub.**


### Why do we need to mock functions?
To answer that question I will introduce the signature of the two methods I will use during this post.

The first function is called *modulo* and it will return 0 if the given number is even, 1 if it is an odd number:
``` c
#ifndef MODULO_H
#define MODULO_H
int modulo(int value);
#endif //MODULO_H
```

The second function is called *both_even* and it will return 0 if both numbers are even, otherwise:
``` c
#ifndef BOTH_H
#define BOTH_H
int both_even(int a, int b);
#endif //BOTH_H
```

Finally, the implementation of the *both_even* is the following:
``` c
#include "both.h"
#include "modulo.h"

int both_even(int a, int b)
{
	int a_m, b_m;
	a_m = modulo(a);
	b_m = modulo(b);
	return a_m == 0 && b_m == 0;
}
```

In this case we will use the *modulo* function to calculate *both_even*, but we do not have the implementation of *modulo*. This is intended because we do not want to use the actual code of the *modulo* function. We want to test **only the code in *both_even***. Therefore, the *modulo* function will be mocked.


### Unit test with FFF
The following code is an example of 6 **unit tests** written using the **FFF** framework:
``` c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "both.h"
#include "modulo.h"
#include "fff.h"
DEFINE_FFF_GLOBALS
#define TEST_F(SUITE, NAME) void NAME()
#define RUN_TEST(SUITE, TESTNAME) printf(" Running %s.%s: \n", #SUITE, #TESTNAME); setup(); TESTNAME(); printf(" SUCCESS\n");

FAKE_VALUE_FUNC1(int, modulo, int);

void setup()
{
	RESET_FAKE(modulo);
}

TEST_F(ModuloTest, both_even_numbers)
{
	int a;
	int b;
	int result;

	// Given
	a = 2;
	b = 4;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 0;
	modulo_fake.return_val_seq[1] = 0;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 0);
}

TEST_F(ModuloTest, first_even_and_second_odd)
{
	int a;
	int b;
	int result;

	// Given
	a = 2;
	b = 3;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 0;
	modulo_fake.return_val_seq[1] = 1;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 1);
}

TEST_F(ModuloTest, first_odd_and_second_even)
{
	int a;
	int b;
	int result;

	// Given
	a = 3;
	b = 2;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 1;
	modulo_fake.return_val_seq[1] = 0;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 1);
}


TEST_F(ModuloTest, both_odd_numbers)
{
	int a;
	int b;
	int result;

	// Given
	a = 3;
	b = 5;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 1;
	modulo_fake.return_val_seq[1] = 1;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 1);
}

TEST_F(ModuloTest, one_even_and_other_zero)
{
	int a;
	int b;
	int result;

	// Given
	a = 2;
	b = 0;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 0;
	modulo_fake.return_val_seq[1] = 0;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 0);
}

TEST_F(ModuloTest, one_odd_and_other_zero)
{
	int a;
	int b;
	int result;

	// Given
	a = 0;
	b = 5;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 0;
	modulo_fake.return_val_seq[1] = 1;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 1);
}

int main(void)
{
	RUN_TEST(ModuloTest, both_odd_numbers);
	RUN_TEST(ModuloTest, both_even_numbers);
	RUN_TEST(ModuloTest, first_even_and_second_odd);
	RUN_TEST(ModuloTest, first_odd_and_second_even);
	RUN_TEST(ModuloTest, one_odd_and_other_zero);
	RUN_TEST(ModuloTest, one_even_and_other_zero);

	return 0;
}
```

On the one hand, the beginning of the code is the initialization of the **FFF** framework and a couple of definitions that will come in handy:
``` c
DEFINE_FFF_GLOBALS
#define TEST_F(SUITE, NAME) void NAME()
#define RUN_TEST(SUITE, TESTNAME) printf(" Running %s.%s: \n", #SUITE, #TESTNAME); setup(); TESTNAME(); printf(" SUCCESS\n");
```

However, the interesting part is:
``` c
FAKE_VALUE_FUNC1(int, modulo, int);
```
The *macro* *FAKE_VALUE_FUNC1* receives three parameters, first the type of the return, second the name of the function to mock and third the type of the parameter. You can find all the information about this in the [documentation](https://github.com/meekrosoft/fff).

On the other hand, each test looks as follows:
``` c
TEST_F(ModuloTest, both_even_numbers)
{
	int a;
	int b;
	int result;

	// Given
	a = 2;
	b = 4;
	modulo_fake.return_val_seq_len = 2;
	modulo_fake.return_val_seq = (int *) malloc(2*sizeof(int));
	modulo_fake.return_val_seq[0] = 0;
	modulo_fake.return_val_seq[1] = 0;

	// When
	result = both_even(a, b);

	// Then
	assert(result != 0);
}
```
And the interesting piece is under the *Given* part. Note that we are configuring the *modulo_fake* struct that contains the information that the *modulo* function will return. Actually, we are saying that it will be called twice and which will be the return values.

The execution of the test will be the following:
``` bash
$ ./run_test 
 Running ModuloTest.both_odd_numbers: 
 SUCCESS
 Running ModuloTest.both_even_numbers: 
 SUCCESS
 Running ModuloTest.first_even_and_second_odd: 
 SUCCESS
 Running ModuloTest.first_odd_and_second_even: 
 SUCCESS
 Running ModuloTest.one_odd_and_other_zero: 
 SUCCESS
 Running ModuloTest.one_even_and_other_zero: 
SUCCESS
```

### Conclusion
**FFF**, or any mocking framework, is an important tool for developers because **it allows to create unit tests for interoperability of different functions**. Furthermore, you can create **unit tests** that are focused on a single function without worring if the functions to which it depends are working properly.
