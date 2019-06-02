+++
title = "ARM C Compiler (ACC)"
description = "img/acc.jpg"
+++

**ACC** is a pet project with the purpose of improving my knowledge of three topics. The C language, compilers and the ARM assembly. I think this is a good exercise to go deep into both topics.

The **ACC** is a **LALR(1) parser**, that means it is a [Look-Ahead Left-to-Right parser](https://en.wikipedia.org/wiki/LALR_parser).

The current **Grammar** of the **ACC** is the following:

```lex
S -> int main "(" ")" "{" E "}"
E -> return I;
     | if "(" B ")" "{" E "}"
     | if "(" B ")" "{" E "}" else "{" E "}"
I -> [0-9]+
B -> I < I
     | I <= I
     | I == I
     | I >= I
     | I > I
     | ! B
     | "(" B ")"
```

### Future work for the project

1. ~~Main function~~
1. ~~Return statement~~
1. ~~Int value~~
1. ~~Boolean operations~~
1. ~~Conditionals~~
1. Variable (int)
1. Addition and substraction operations
1. Multiplication and division operations
1. Comments
1. Functions
1. String
1. Array
1. Pointer
1. Struct
1. Loop
1. Include
1. ...
1. Self-contained Compiler

### Example of the usage of the ACC

C code:

```c
int main()
{
    if (1 < 2)
    {
	    if (4 > 10)
	    {
		    return 1;
	    }
	    else {
		    return 2;
	    }
    }
    return 0;
}
```

Assembly generated:

```
	.text
	.global main
main:
	mov r0, #1
	mov r1, #2
	cmp r0, r1
	bge if_else_0
	mov r0, #4
	mov r1, #10
	cmp r0, r1
	ble if_else_1
	mov r0, #1
	bx lr
if_else_1:
	mov r0, #2
	bx lr
if_else_0:
	mov r0, #0
        bx lr
```