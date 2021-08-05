+++
title = "Software development using BASH"
date = "2019-11-24T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Bash", "Static Analysis", "Unit Test"]
categories = ["Development"]
+++

As for any other language I develop with, **I like to make use of tools and utilities to
help me spot problems as soon as possible.**

For that reason I like to have three things in all my projects:

* Formatter
* Linter (Static Analysis)
* Unit Test Framework

When developing in `Bash` there is no difference in this regard. Some people would say
that `Bash` is *just* for scripting. I mostly agree with that statement,
however, **sometimes you have to write a lot of `Bash` and for these cases I want
to be able to develop it in the same way I do for other languages.**

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/bash_2018_02_24).**

### Formatter

A formatter's duty is to keep the code style the same across a whole project. For
`Bash` I like to use [shfmt](https://github.com/mvdan/sh) as the formatter. It
is a `Go` project and it can be installed running

```bash
go get -u mvdan.cc/sh/cmd/shfmt
```

The most basic usage for `shfmt` is to format a file. By default it targets
`bash`, but to target just `POSIX` compatible shells the flag `-p` can be used.

An example file before formatting:

```bash
#!/bin/bash

echo "Welcome to this example file"
    echo "This is badly formatted"




  VAR=$( pwd )

echo "This script is being ran from ${VAR}"



for item       in   $(seq 1 10)
do
  echo "Number ${item}"
done
```

The previous file formatted:

```bash
$ shfmt mess.sh 
#!/bin/bash

echo "Welcome to this example file"
echo "This is badly formatted"

VAR=$(pwd)

echo "This script is being ran from ${VAR}"

for item in $(seq 1 10); do
	echo "Number ${item}"
done
```

Two interesting options I use quite often with `shfmt` are `-bn` and `-ci`. They
are for **binary operations like `&&` and `|` may start a line** and **switch
cases will be indented**, respectively. 

An example script with binary operations and a switch case:

```bash
#!/bin/bash

first_thing_to_be_run \
&& second_thing_to_be_run \
&& third_thing_to_be_run \
&& forth_and_last_thing_to_be_run

number=$RANDOM
case ${number} in
5)
echo "Lucky number"
;;
7)
echo "Lucky number"
;;
*)
echo "It may not be a lucky number"
;;
esac
```

`shfmt` run with default arguments:

```bash
$ shfmt binary_ops_and_switch_cases.sh
#!/bin/bash

first_thing_to_be_run &&
	second_thing_to_be_run &&
	third_thing_to_be_run &&
	forth_and_last_thing_to_be_run

number=$RANDOM
case ${number} in
5)
	echo "Lucky number"
	;;
7)
	echo "Lucky number"
	;;
*)
	echo "It may not be a lucky number"
	;;
esac
```

`shfmt` run with `-bn` and `-ci` flags:

```bash
$ shfmt -bn -ci binary_ops_and_switch_cases.sh
#!/bin/bash

first_thing_to_be_run \
	&& second_thing_to_be_run \
	&& third_thing_to_be_run \
	&& forth_and_last_thing_to_be_run

number=$RANDOM
case ${number} in
	5)
		echo "Lucky number"
		;;
	7)
		echo "Lucky number"
		;;
	*)
		echo "It may not be a lucky number"
		;;
esac
```

### Linter (Static Analysis)

Any good linter's job is to point out all the errors that can found in your code. My favourite `Bash` linter is `ShellCheck`. It can be used from their website [https://www.shellcheck.net/](https://www.shellcheck.net/) or installing their command line application in your system.

Can you spot all the errors in the following snippet?

```bash
#!/bin/sh

for file in $(ls *.py); do
	grep -qi wololo* $file \
		&& echo -e 'The file $file contains words that start with wololo'
done
```

I am sure you have found several errors, but let's have a look at the output of `ShellCheck`

```bash
$ shellcheck errors.sh 

In errors.sh line 3:
for file in $(ls *.py); do
            ^-- SC2045: Iterating over ls output is fragile. Use globs.
                 ^-- SC2035: Use ./*.py so names with dashes won't become options.


In errors.sh line 4:
	grep -qi wololo* $file \
                 ^-- SC2062: Quote the grep pattern so the shell won't interpret it.
                 ^-- SC2022: Note that unlike globs, o* here matches 'ooo' but not 'oscar'.
                         ^-- SC2086: Double quote to prevent globbing and word splitting.


In errors.sh line 5:
		&& echo -e 'The file $file contains words that start with wololo'
                        ^-- SC2039: In POSIX sh, echo flags are not supported.
                           ^-- SC2016: Expressions don't expand in single quotes, use double quotes for that.
```

Finding errors like these by just looking at the code is hard. So, let a computer do
it for you.

### Unit Test Framework

Last but not least, a unit test framework for `Bash`. My choice is [Bats](https://github.com/sstephenson/bats).

Given the following `functions.sh` file:

```bash
sum() {
  if [ ${#} -ne 2 ]; then
    echo "Bad number of parameters"
    echo "Usage: sum <number 1> <number 2>"
  else
    num1=${1}; shift
    num2=${1}; shift
    echo "${num1}+${num2}" | bc
  fi
}
```

Test file `test_functions.sh` for the previous file:

```bash
#!/usr/bin/env bats

source functions.sh

@test "The addition of 4 and 5 results in 9" {
  run sum 4 5
  [ "$status" -eq 0 ]
  [ "${#lines[@]}" -eq 1 ]
  [ "${lines[0]}" = "9" ]
}

@test "The addition of -5 and 9 results in 4" {
  run sum -5 9
  [ "$status" -eq 0 ]
  [ "${#lines[@]}" -eq 1 ]
  [ "${lines[0]}" = "4" ]
}

@test "Bad number of parameters (1)" {
  run sum 10
  [ "$status" -eq 0 ]
  [ "${#lines[@]}" -eq 2 ]
  [ "${lines[0]}" = "Bad number of parameters" ]
  [ "${lines[1]}" = "Usage: sum <number 1> <number 2>" ]
}

@test "Bad number of parameters (3)" {
  run sum 10 11 12
  [ "$status" -eq 0 ]
  [ "${#lines[@]}" -eq 2 ]
  [ "${lines[0]}" = "Bad number of parameters" ]
  [ "${lines[1]}" = "Usage: sum <number 1> <number 2>" ]
}
```

When that battery of test is run it outputs:

```bash
$ ./test_functions.sh 
 ✓ The addition of 4 and 5 results in 9
 ✓ The addition of -5 and 9 results in 4
 ✓ Bad number of parameters (1)
 ✓ Bad number of parameters (3)

4 tests, 0 failures
```

### Conclusion

`Bash` is a great scripting language, but **when you have to write more than a
simple script to perform a task it is worth spending the time in using a formatter,
a linter and unit test framework**. It may be even useful to use some
documentation generation tool as well.
