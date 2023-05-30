+++
title = "rr debugger, an improvement over GDB"
date = "2016-01-15T13:50:46+02:00"
author = "Oscar Forner"
tags = ["GDB", "rr", "Debugger", "C", "C++"]
categories = ["Development"]
+++

## Introduction

**rr** is a debugging tool from Mozilla that **enhances the behaviour of GDB**. It can be found in
[GitHub](https://github.com/mozilla/rr), but my recomendation is to go first to the website of the
[project](http://rr-project.org/). In the website you can find really useful information and documentation.

As usual, I am working from an Arch Linux computer. Therefore, I can install **rr** from the AUR repository (rr). For other distributions you can find the information in the documentation.

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/rr_debugger_gdb_post_2016_01_15/src)**.

The videos are made with **[asciinema](https://asciinema.org/)**, that means **you can copy from the video**.

## Before starting debugging

It is recommended to have your CPU frequency governor in 'performance' mode instead of 'powersave'. Because of that, it is recommended to set it:

``` bash
sudo cpufreq-set -g performance
```

To set it back to 'powersave' mode just run:

``` bash
sudo cpufreq-set -g powersave
```

## How **rr** works

**rr** works in two phases. In the first one, it *records* the execution of a program. In the second one, it *replays* the execution of that program as many times as you need. Moreover, during the *replay* phase **you can go forward and backward in the execution**.

**rr** adds some new commands to **GDB** such as *reverse-next* or *reverse-continue*. I think these commands do not need more explanation.

## Example of usage

In this example I will use the following code:

``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[]) {

	if (argc != 2) {
		fprintf(stderr, "Error: Bad number of parameters\n");
		fprintf(stderr, "Usage: %s <how many times>", argv[0]);
		return -1;
	}

	int num = atoi(argv[1]);
	int input = 0;
	int acum = 0;
	for (int i = 0; i < num; ++i) {
		printf("Next one: ");
		scanf("%d", &input);
		acum += input;
	}

	printf("Total acumulated: %d\n", acum);
	return 0;
}
```

It will be compiled with the *-g* to produce debugging information as you would do for **GDB**:

``` bash
gcc main.c -g -o app
```

### Record of the execution

In the following video it will be shown how to record the execution of an application.
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/5m0lpbkqj6xyl9fy0ath9tnjd.js" id="asciicast-5m0lpbkqj6xyl9fy0ath9tnjd" async></script>
{{< /rawhtml >}}

### Replay of the execution

In the folowwing video it will be shown how to replay the execution of an application.
{{< rawhtml >}}
<script type="text/javascript" src="https://asciinema.org/a/cpzdimjm3v3ghownpynzey1bu.js" id="asciicast-cpzdimjm3v3ghownpynzey1bu" async></script>
{{< /rawhtml >}}

## Conclusion

Personally, I consider **rr** a **must have** tool for debugging. The ability to go backwards in the execution at any time is extremely useful when you are trying to find the exact moment where something starts to go wrong. Moreover, the fact that you do not have to keep providing any kind of input to the app is really good to focus just in the execution.
