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
This post is a continuation from a previous post called [Unit test with Google Test for C++](http://maitesin.github.io//GoogleTest-C++/), but in this post we are going to use **Google Mock**, that extends the functionality of **Google Test**.

**Google Mock** is one of the available frameworks for C++ to mock objects in **unit tests**. In this example I will use the same technologies as for the previous one: **CMake** to configure the project and build it, for the **dependency manager** I will use the new and shiny **[conan](https://www.conan.io/)**.

**All the code and configuration files used in this post are available in this [repo](https://github.com/maitesin/blog/tree/master/google_mock_2016_01_22) in GitHub.**

### Why do we need to mock objects?
To answer that question I will introduce the two classes I will use during this post.


The first class is called *Producer* and it will extract the domain of a given URL:
``` cpp
#ifndef PRODUCER_H
#define PRODUCER_H

#include <string>

class Producer {
public:
	virtual ~Producer(){}
	virtual std::string getDomainFromUrl(const std::string & url) const = 0;
};

#endif /*PRODUCER_H*/
```

The second class is called *Consumer* and it will calculate the level of the domain of a given URL:
``` cpp
#ifndef CONSUMER_H
#define CONSUMER_H

#include <string>
#include <algorithm>
#include "producer.h"

class Consumer {
public:
	Consumer(Producer * p): producer(p){}
	int countLevelOfDomain(const std::string & url) const {
		std::string domain = producer->getDomainFromUrl(url);
		return std::count(domain.begin(), domain.end(), '.') + 1;
	}
private:
	Producer * producer;
};

#endif /*CONSUMER_H*/
```

In this case we want to create a unit test for the *Consumer* class, but we need to implement a *Producer* class for that, right? Well, no. **We do not need an implementation of the *Producer* class because we can mock it**. Moreover, in that case the unit test would not be only for the *Consumer* class, but for the *Producer* too, and that is not what we are looking for.


### Unit test with Google Mock
The following unit test is written using the **Google Mock** framework:
``` cpp
#include <string>
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "producer.h"
#include "consumer.h"

class ProducerMock : public Producer {
public:
	MOCK_CONST_METHOD1( getDomainFromUrl, std::string(const std::string & url) );
};

TEST(Consumer, CalculateDomainLevel) {
	const std::string url = "http://www.fantasticdomain.com/site/index.html";
	std::string domain = "fantasticdomain.com";
	ProducerMock mock;
	Consumer consumer(&mock);
	EXPECT_CALL(mock, getDomainFromUrl(url))
		    .WillOnce(::testing::Return(domain));
	int domainLevel = consumer.countLevelOfDomain(url);
	EXPECT_EQ(domainLevel, 2);
}

int main(int argc, char **argv) {
	testing::InitGoogleMock(&argc, argv);
	return RUN_ALL_TESTS();
}
```

On the one hand, the *ProducerMock* class is inheriting from the *Producer* class. However, the interesting part is
``` cpp
MOCK_CONST_METHOD1( getDomainFromUrl, std::string(const std::string & url) );
```
The line above is telling **Google Mock** to mock the method *getDomainFromUrl* from the *Producer* class and it will receive a *const std::string* by reference as parameter and it will return a *std::string* by value.


On the other hand, there is the *EXPECT_CALL* macro that receives two parameters:
``` cpp
EXPECT_CALL(mock, getDomainFromUrl(url))
                   .WillOnce(::testing::Return(domain));
```
The first parameter is the mocked object and second one is the method that will be called and **the parameter that will be passed**. The result of the expansion of the macro will call a method called *WillOnce* that will make the mocked object answer once to the method. Finally, *::testin::Return(domain)* specifies the return of that call, which will be *domain*.


The execution of the test will be the following:
``` bash
$ ./bin/run_test 
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from Consumer
[ RUN      ] Consumer.CalculateDomainLevel
[       OK ] Consumer.CalculateDomainLevel (0 ms)
[----------] 1 test from Consumer (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (0 ms total)
[ PASSED ] 1 test.
```

### Conclusion
**Google Mock**, or any mocking framework, is an important tool for developers because **it allows to create unit tests for interoperability of different objects**. Furthermore, you can create **unit tests** that are focused on a single class without worring if the class to which it depends is working properly.
