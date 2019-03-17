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
**Boost ASIO** library is the *defacto standard* for **network** and **low-level I/O programming**. It has a **great documentation available online**, but there are a lot of methods and classes in the library. Therefore, if it is your first attempt to use it, it can be a bit challenging.

Since there is a lot of ground to cover in the **Boost ASIO** library, I will only cover the **work scheduler** and the **synchronous** methods in this post. The **asynchronous** methods and **timers** will be covered in following posts.

During this post I use **CMake** to configure and build the project and as **dependency manager** I will use **[conan](https://www.conan.io/)**.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/boost_asio_2017_01_21)**.

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

### IO Service
The **IO Service** is the mainstay of the **Boost ASIO**. Basically, it is in charge of scheduling the work to be done. In this section, I will use the **IO Service** to demonstrate how it performs the scheduling. However, it is not recommended to use it for this purpose, as [**Sean Parent** shows in this talk](https://www.youtube.com/watch?v=QIHy8pXbneI).

**The whole idea of this section is to help you understand how the Boost ASIO works underneath.**

#### One worker
The code for this simple example is to just show how the **IO Service** can perform some work.
``` cpp
#include <iostream>
#include <boost/asio.hpp>

int main()
{
  boost::asio::io_service service;

  service.post([](){std::cout << "1" << std::endl;});
  service.post([](){std::cout << "2" << std::endl;});
  service.post([](){std::cout << "3" << std::endl;});
  service.post([](){std::cout << "4" << std::endl;});
  service.post([](){std::cout << "5" << std::endl;});
  service.post([](){std::cout << "6" << std::endl;});

  service.run();

  return 0;
}
```
The code is quite straightforward, it provides 6 tasks to the **IO Service** and then it executes them.

##### Execution
The output of the previous code is what everybody can expect.
<script type="text/javascript" src="https://asciinema.org/a/1bwz66y6imztewkt2kriaqnjh.js" id="asciicast-1bwz66y6imztewkt2kriaqnjh" async></script>

#### Two workers
The code for the two workers is a bit more complicated. The idea is the same, but with two threads executing tasks instead of one.
``` cpp
#include <iostream>
#include <vector>
#include <thread>
#include <algorithm>
#include <boost/asio.hpp>

int main()
{
  std::vector<std::thread> worker;
  boost::asio::io_service service;

  service.post([](){std::cout << "1" << std::endl;});
  service.post([](){std::cout << "2" << std::endl;});
  service.post([](){std::cout << "3" << std::endl;});
  service.post([](){std::cout << "4" << std::endl;});
  service.post([](){std::cout << "5" << std::endl;});
  service.post([](){std::cout << "6" << std::endl;});

  for (int i = 0; i < 2; i++) {
    worker.push_back(std::thread([&](){ service.run(); }));
  }

  std::for_each(std::begin(worker), std::end(worker), [](std::thread &t){t.join();});

  return 0;
}
```
The complexity of the previous code is the usage of threads, but it is not overwhelming.

##### Execution
The output of the *two workers* code can be the same as from the *one worker* section. However, it is not guaranteed that it would be the same. This can be seen in the following execution:
<script type="text/javascript" src="https://asciinema.org/a/da8dspoce5ud1k1a49rm9qlzm.js" id="asciicast-da8dspoce5ud1k1a49rm9qlzm" async></script>

### Synchronous
In order to use **Boost ASIO** for **network** it is not required to know how the **IO Service** works. Actually, the explicit usage of **IO Service** as it is done in the previous section is not recommended.

In this section, the usage of **synchronous** calls is shown in order to create a **client** and a **server** programs.

#### Client
The code for the client sends a message - provided as a parameter - to the server. After that the client reads the answer from the server and prints it in the standard output.
``` cpp
#include <iostream>
#include <string>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

int main(int argc, const char *argv[])
{
  // Check provided parameters
  if (argc != 4) {
    std::cerr << "Error. Bad number of parameters" << std::endl;
    std::cerr << "Usage: " << argv[0] << " <hostname> <port|service> <message>" << std::endl;
    exit(-1);
  }

  // Error to not throw exception
  boost::system::error_code not_throw;

  // Resolve hostname and port
  boost::asio::io_service service;
  tcp::resolver resolver(service);
  tcp::resolver::query query(argv[1], argv[2]);
  tcp::resolver::iterator endpoint = resolver.resolve(query, not_throw);
  if (not_throw) {
    std::cerr << "Error resolving host(" << not_throw.value() << "): "<< not_throw.message() << std::endl;
    return 1;
  }

  // Socket and connection
  tcp::socket socket(service);
  boost::asio::connect(socket, endpoint, not_throw);
  if (not_throw) {
    std::cerr << "Error connecting(" << not_throw.value() << "): "<< not_throw.message() << std::endl;
    return 1;
  }

  // Send a message to the end point
  std::string message = {argv[3]};
  socket.write_some(boost::asio::buffer(message), not_throw);
  if (not_throw) {
    std::cerr << "Error sending(" << not_throw.value() << "): "<< not_throw.message() << std::endl;
    return 1;
  }

  // Read a message from the end point
  boost::asio::streambuf response;
  boost::system::error_code error = boost::asio::error::eof;
  do {
    boost::asio::read(socket, response, error);
  } while(error && error != boost::asio::error::eof);

  // Close socket
  socket.close();

  // Show the received message
  std::istream received(&response);
  std::cout << received.rdbuf() << std::endl;

  return 0;
}
```

The first interesting part of the code is the *resolution of the hostname and the port*. Pay attention to the fact that the "port" is a string. It is because it can be a number or a service name (i.e. "https" as port would connect to port 443).
``` cpp
  // Resolve hostname and port
  boost::asio::io_service service;
  tcp::resolver resolver(service);
  tcp::resolver::query query(argv[1], argv[2]);
  tcp::resolver::iterator endpoint = resolver.resolve(query, not_throw);
  if (not_throw) {
    std::cerr << "Error resolving host(" << not_throw.value() << "): "<< not_throw.message() << std::endl;
    return 1;
  }
```

The next interesting part of the code is the *send of the message to the end point*. The interesting bit is how the data is send. In this case, the message is stored in a *std::string*, but it is required to be transformed into a *boost::asio::buffer*.
``` cpp
  // Send a message to the end point
  std::string message = {argv[3]};
  socket.write_some(boost::asio::buffer(message), not_throw);
  if (not_throw) {
    std::cerr << "Error sending(" << not_throw.value() << "): "<< not_throw.message() << std::endl;
    return 1;
  }
```

The last interesting part of the code is the *read a message from the end point*. In this case, a *boost::asio::streambuf* is used to retrieve the data from the server. However, it could have been done in other ways as it is shown in the **server** case. The errors are another interesting part of the code.  The "success" error (when the first part of the conditional is false) will happen when the buffer is full. However, the *boost::asio::error::eof* will occur when the end point closes the connection.
``` cpp
  // Read a message from the end point
  boost::asio::streambuf response;
  boost::system::error_code error = boost::asio::error::eof;
  do {
    boost::asio::read(socket, response, error);
  } while(error && error != boost::asio::error::eof);
```

#### Server
The code for the server receives a message, then it returns the message backwards to the sender.
``` cpp
#include <iostream>
#include <string>
#include <algorithm>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

int main(int argc, const char *argv[])
{
  // Check provided parameters
  if (argc != 2) {
    std::cerr << "Error. Bad number of parameters" << std::endl;
    std::cerr << "Usage: " << argv[0] << " <port>" << std::endl;
    exit(-1);
  }
  // Get the port from the parameters
  uint16_t port = std::stoul(argv[1]);

  // Error to not throw exception
  boost::system::error_code not_throw;

  // Socket and acceptor
  boost::asio::io_service service;
  tcp::acceptor acceptor(service, tcp::endpoint(tcp::v4(), port));
  tcp::socket socket(service);
  acceptor.accept(socket, not_throw);
  if (not_throw) {
    std::cerr << "Error when binding the port in the socket" << std::endl;
    return 1;
  }

  // Read a message
  size_t size;
  char buf[512];
  std::ostringstream oss;
  boost::system::error_code error = boost::asio::error::eof;
  do {
    size = socket.read_some(boost::asio::buffer(buf), error);
    oss << std::string(buf, sizr);
  } while(error && error != boost::asio::error::eof);

  // Reverse the received message
  std::string original = oss.str();
  std::reverse(std::begin(original), std::end(original));

  // Write the reversed message
  socket.write_some(boost::asio::buffer(original), not_throw);
  if (not_throw) {
    std::cerr << "Error sending(" << not_throw.value() << "): " << not_throw.message() << std::endl;
    return 1;
  }

  // Close socket
  socket.close();

  return 0;
}
```

The first interesting part of the code is the *socket and acceptor*. In this case the port is a number. Another good part is how the usage of IPv4 only has been specified.
``` cpp
  // Socket and acceptor
  boost::asio::io_service service;
  tcp::acceptor acceptor(service, tcp::endpoint(tcp::v4(), port));
  tcp::socket socket(service);
  acceptor.accept(socket, not_throw);
  if (not_throw) {
    std::cerr << "Error when binding the port in the socket" << std::endl;
    return 1;
  }
```

The last interesting part of the code is the *read a message*. In this case, it is using a plain *char* array to read parts of the message and store it in a *std::ostringstream*. Pay attention to how it keeps track of the amount of data that has been read and stores that much information only.
``` cpp
  // Read a message
  size_t size;
  char buf[512];
  std::ostringstream oss;
  boost::system::error_code error = boost::asio::error::eof;
  do {
    size = socket.read_some(boost::asio::buffer(buf), error);
    oss << std::string(buf, size);
} while(error && error != boost::asio::error::eof);
```

#### Execution
<script type="text/javascript" src="https://asciinema.org/a/10bf5yr6qyuqh5oxm2ru65qlr.js" id="asciicast-10bf5yr6qyuqh5oxm2ru65qlr" async></script>

### Conclusion
**The simplicity of the Boost ASIO is matched only by its power**. It is quite simple to create a **synchronous** **client/server** application. These are the basics of **Boost ASIO** and it should allow you to understand more complex usage of it.
