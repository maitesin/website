+++
title = "Thread, Future, and Promise"
date = "2016-09-11T13:50:46+02:00"
author = "Oscar Forner"
tags = ["C++", "Concurrency", "Future", "Promise", "Thread"]
categories = ["Development"]
+++

## Introduction

In the C++11 standard several **concurrency** related classes were added. I will talk about **thread**, **future** and **promise**. Yes, I know there are others more useful than these three. However, **I think that it is really important to know well the bases to be able to use the more complex ones properly**.

As usual, I am working from an Arch Linux computer. Therefore, I can install **Clang** and the tools from the repository (clang). For other distributions you can find the information in the documentation.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/future_and_promise_2016_09_11)**.

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

## Thread

**Thread** is the basic element of **concurrency** in the C++11 standard and they are intended to map one-to-one the operating system's threads.

### Simple

In this example we use a **thread** to perform the task done by the function *accum_up_to*.

``` cpp
#include <iostream>
#include <functional>
#include <thread>

void accum_up_to(int value, int & result) {
  int accum = 0;
  for (int i = 0; i <= value; ++i) {
    accum += i;
  }
  result = accum;
}

int main()
{
  int result;
  std::thread t1(accum_up_to, 50, std::ref(result));

  t1.join();

  std::cout << "Calculated a value of: " << result << std::endl;

  return 0;
}
```

Some parts to note in the code are the following:

* The function that is executing the **thread** has a return type of void. Therefore, to get a result from that function it is required to provide a parameter to hold it.
* Before being able to use the result stored in the parameters passed we have to make sure the thread has finished. To do so we use the *join* method of the **thread** to synchronize it.

#### Execution

<script type="text/javascript" src="https://asciinema.org/a/0i676ob9b1btu4bosdno69d1d.js" id="asciicast-0i676ob9b1btu4bosdno69d1d" async></script>

### Two threads

In this example we use two **threads** that perform the same task done by the function *accum_up_to*.

``` cpp
#include <iostream>
#include <functional>
#include <thread>

void accum_up_to(int value, int & result) {
  int accum = 0;
  for (int i = 0; i <= value; ++i) {
    accum += i;
  }
  result = accum;
}

int main()
{
  int result1, result2;
  std::thread t1(accum_up_to, 50, std::ref(result1));
  std::thread t2(accum_up_to, 40, std::ref(result2));

  t1.join();
  t2.join();

  std::cout << "Calculated a value of: " << result1 << std::endl;
  std::cout << "Calculated a value of: " << result2 << std::endl;

  return 0;
}
```

As you can see above once the code is able to hold a thread, it is quite easy to make it hold two. However, **now we have two result variables and two calls to the method join**. As you can see it is not really easy to keep track once you have several **threads**.

#### Execution
<script type="text/javascript" src="https://asciinema.org/a/4xl3gxqtgch0cx4cmjuym6kkq.js" id="asciicast-4xl3gxqtgch0cx4cmjuym6kkq" async></script>

## Future

**Future** provides a way to access the result of asynchronous operations. You can imagine we use this to avoid the tedious part of getting the results from the **threads**.

### Simple

In this example we use a **future** to perform the task done by the function *accum_up_to*.

``` cpp
#include <iostream>
#include <future>

int accum_up_to(int value) {
  int accum = 0;
  for (int i = 0; i <= value; ++i) {
    accum += i;
  }
  return accum;
}


int main()
{
  std::future<int> f = std::async(std::launch::async, accum_up_to, 50);

  std::cout << "Calculated a value of: " << f.get() << std::endl;

  return 0;
}
```

Some changes compared to the **thread** version:

* The function returns the value directly and it can be accesed by the method *get*. Moreover, the method *get* synchronizes the **future**.
* **Future** is gotten from the *async* function. This is really similar to how the **threads** are created.

#### Execution
<script type="text/javascript" src="https://asciinema.org/a/9tk2efdt4dbbf1wesc4oo3bue.js" id="asciicast-9tk2efdt4dbbf1wesc4oo3bue" async></script>

### Two futures

In this example we use two **futures** that perform the same task done by the function *accum_up_to*.

``` cpp
#include <iostream>
#include <future>

int accum_up_to(int value) {
  int accum = 0;
  for (int i = 0; i <= value; ++i) {
    accum += i;
  }
  return accum;
}


int main()
{
  std::future<int> f1 = std::async(std::launch::async, accum_up_to, 50);
  std::future<int> f2 = std::async(std::launch::async, accum_up_to, 40);

  std::cout << "Calculated a value of: " << f1.get() << std::endl;
  std::cout << "Calculated a value of: " << f2.get() << std::endl;

  return 0;
}
```

**This time the execution of two tasks in separate threads is way cleaner**.

#### Execution
<script type="text/javascript" src="https://asciinema.org/a/bzll7syk13m2yas2nf3p3exrg.js" id="asciicast-bzll7syk13m2yas2nf3p3exrg" async></script>


## Promise

**Promise** is where a task can deposit its result to be retrieved through a **future**. In other words, **promise** is a way to have a single point of synchronization between two **threads** without being the end of one of them.

### Simple

In this example we use a **promise** to send some information (from the user) into a **future** to perform the task done by the function *accum_up_to*.

``` cpp
#include <iostream>
#include <functional>
#include <thread>
#include <future>

void accum_up_to(std::future<int>& f) {
  std::cout << "Started accum_up_to method" << std::endl;
  int accum = 0;
  int value = f.get();
  for (int i = 0; i <= value; ++i) {
    accum += i;
  }
  std::cout << "Calculated a value of: " << accum << std::endl;
}


int main()
{
  int limit;
  std::promise<int> p;
  std::future<int> f = p.get_future();
  std::thread t(accum_up_to, std::ref(f));

  std::cout << "Introduce the limit:" << std::endl;
  std::cin >> limit;

  p.set_value(limit);
  t.join();

  return 0;
}
```

Some key points from the example:

* The **promise** provides you a **future** and that **future** is used by the *accum_up_to* function.
* Once the user gives a number, the **promise** sends it to the **future**, as it is waiting for the number where the *get* method is called.
* Finally, the method *join* from the **thread** is called in order to wait for it to finish the execution of the function *accum_up_to*.

#### Execution
<script type="text/javascript" src="https://asciinema.org/a/6so6sj02g30yns7rqmc5rr9zp.js" id="asciicast-6so6sj02g30yns7rqmc5rr9zp" async></script>
In this execution something called **data race** is shown. That can be seen because the execution of the same program can generate different outputs (even if the result value is always the same).

## Conclusion

These are **really** the basics of **concurrency** that are provided in the C++11 standard. I know there are other important topics from **concurrency** such as **mutex** or **condition variable** and I will talk about them in the future because they deserve their own post. Futhermore, I know I have not talked about **data races**, **dead locks** and all the other problems you face when doing **concurrency**, again if people are interested in this topic I can write about it too.
