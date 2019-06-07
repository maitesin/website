+++
title = "ARM C Compiler (ACC) I"
date = "2016-02-12T13:50:46+02:00"
author = "Oscar Forner"
tags = ["ARM", "C"]
categories = ["Development"]
+++

**Why do you want to create your own compiler?** To answer this question I have to give you some background. For Christmas I got a **BeagleBone Black**, perfect to **learn ARM assembly**. After a few weeks of doing the usual stuff I decided I wanted a bigger project to improve my knowledge. However, the idea to start the **development of a compiler** comes from [http://www.sigbus.info/how-i-wrote-a-self-hosting-c-compiler-in-40-days.html](http://www.sigbus.info/how-i-wrote-a-self-hosting-c-compiler-in-40-days.html).

**The only aim of this project is to improve my knowledge of the ARM assembly, the C language and Compilers**. The project can be found in [GitHub](https://github.com/maitesin/acc).

### What is the target of the project?

My target is to have a **self-hosting compiler of C**. For this reason I want to **keep it simple**. Moreover, I will only develop the features I need to accomplish the target of the project. As you can imagine the choosen language is C (ANSI C to be specific).

I decided **not to use Flex, Bison, Lex or Yacc** because I want to work in all stages of the compiler. Yes, it sounds crazy and maybe I will regret it in the future, but at least I will try it.

### What is the current state of the project?

Currently, I have implemented a **very basic compiler**, this version is available in [GitHub as v0.1](https://github.com/maitesin/acc/tree/v0.1). *It just generates code for a file containing the main function without parameters and the body only contains a return statement of a positive integer*.

#### Structure of the project

The project contains three folders:

* *inc*: holds the external libraries needed. Right now, it has the files of **Unity** for unit testing.
* *unittest*: has the unit tests for the project. It has just one, but once I find a good framework to do mocks in C, it will have more unit tests.
* *src*: contains the actual source code of the project.

This compiler is made of a **Lexer** that creates **Tokens**. These **Tokens** are used by the **Grammar** to create **AST nodes**. Finally, the **AST nodes** will be used by the **Generator** to generate the assembly.

##### Lexer and Tokens

The available **Tokens** are: *int_value*, *int_type*, *function*, *open_parenthesis*, *close_parenthesis*, *open_bracket*, *close_bracket*, *return*, *semicolon* and *end_of_file*. These can be found in the file *tokens.h*:

``` c
#ifndef TOKEN_H
#define TOKEN_H

#include <stdlib.h>

enum token_type {
	T_INT_TYPE,
	T_INT_VALUE,
	T_FUNCTION,
	T_OPAR,
	T_CPAR,
	T_OBRA,
	T_CBRA,
	T_RETURN,
	T_SEMICOLON,
	T_END_OF_FILE
};

/*
 * Tokens for the parser
 */
typedef struct token_base
{
	enum token_type type;
	void * token_pointer;
} token_base;

typedef struct token_int_type
{
	token_base base;
} token_int_type;

typedef struct token_int_value
{
	token_base base;
	int value;
} token_int_value;

typedef struct token_function
{
	token_base base;
	char * name;
} token_function;

typedef struct token_opar
{
	token_base base;
} token_opar;

typedef struct token_cpar
{
	token_base base;
} token_cpar;

typedef struct token_obra
{
	token_base base;
} token_obra;

typedef struct token_cbra
{
	token_base base;
} token_cbra;

typedef struct token_return
{
	token_base base;
} token_return;

typedef struct token_semicolon
{
	token_base base;
} token_semicolon;

typedef struct token_eof
{
	token_base base;
} token_eof;

/*
 * Init functions for the tokens
 */
void init_token_int_type(token_int_type * token);
void init_token_int_value(token_int_value * token, int  value);
void init_token_function(token_function * token, char * name);
void init_token_opar(token_opar * token);
void init_token_cpar(token_cpar * token);
void init_token_obra(token_obra * token);
void init_token_cbra(token_cbra * token);
void init_token_return(token_return * token);
void init_token_semicolon(token_semicolon * token);
void init_token_eof(token_eof * token);

/*
 * Release functions for the tokens
 */
void free_token_int_type(token_int_type * token);
void free_token_int_value(token_int_value * token);
void free_token_function(token_function * token);
void free_token_opar(token_opar * token);
void free_token_cpar(token_cpar * token);
void free_token_obra(token_obra * token);
void free_token_cbra(token_cbra * token);
void free_token_return(token_return * token);
void free_token_semicolon(token_semicolon * token);
void free_token_eof(token_eof * token);
#endif //TOKEN_H
```

These **Tokens** are returned by the method *next* from the **Lexer** in the file *lexer.h*:

``` c
#ifndef LEXER_H
#define LEXER_H

#include <stdio.h>
#include "token.h"

typedef struct lexer
{
	FILE * f;
} lexer;

void init_lexer(lexer * l, const char * filename);
void destroy_lexer(lexer * l);
struct token_base * next(lexer * l);

#endif //LEXER_H
```

##### Grammar and AST nodes

The available **AST nodes** are: *id*, *int*, *function* and *return*. These can be found in the file *ast.h*:

``` c
#ifndef AST_H
#define AST_H

#include <stdlib.h>

enum ast_type {
	A_ID,
	A_INT,
	A_FUNCTION,
	A_RETURN
};

/*
 * AST nodes
 */
typedef struct ast_base
{
	enum ast_type type;
	void * ast_pointer;
} ast_base;

typedef struct node_id
{
	ast_base base;
	char * value;
} node_id;

typedef struct node_int
{
	ast_base base;
	int value;
} node_int;

typedef struct node_function
{
	ast_base base;
	char * name;
	ast_base * entry_point;
} node_function;

typedef struct node_return
{
	ast_base base;
	ast_base * value;
} node_return;

/*
 * Init functions for the AST nodes
 */
void init_node_id(node_id * node, char * value);
void init_node_int(node_int * node, int value);
void init_node_function(node_function * node, char * name, ast_base * entry_point);
void init_node_return(node_return * node, ast_base * value);

/*
 * Release functions for the AST nodes
 */
void free_node_id(node_id * node);
void free_node_int(node_int * node);
void free_node_function(node_function * node);
void free_node_return(node_return * node);
#endif //AST_H
```

The **AST** is returned by the method *build_ast* from the **Grammar** in the file *grammar.h*:

``` c
#ifndef GRAMMAR_H
#define GRAMMAR_H

#include <stdio.h>
#include "lexer.h"
#include "ast.h"

typedef struct grammar
{
	lexer * l;
} grammar;

void init_grammar(grammar * g, lexer * l);
ast_base * build_ast(grammar * g);
void destroy_grammar(grammar * g);


/*
 * Read functions to build AST parts
 */
ast_base * read_function_ast_node(grammar * g);
ast_base * read_function_body(grammar * g);
#endif //GRAMMAR_H
```

##### Generation of assembly

The **Generator** has a **Grammar** that will be used to generate the assembly with the method *generate_code*:

``` c
#ifndef GENERATOR_H
#define GENERATOR_H

#include <stdio.h>
#include "grammar.h"

typedef struct generator
{
	grammar * g;
	FILE * f;
} generator;

// API
void init_generator(generator * gen, grammar * gra, const char * out);
void destroy_generator(generator * g);
void generate_code(generator * g);

// Internals
void __generate_code(generator * g, ast_base * ast);
void __generate_code_for_main(generator * g, ast_base * ast);
void __generate_code_for_function(generator * g, node_function * ast);
void __generate_code_for_return(generator * g, node_return * ast);
void __generate_code_for_int(generator * g, node_int * ast);

#endif //GENERATOR_H
```

### Example of the current functionality

The code to be compiled into ARM assembly is:

``` c
int main()
{
	return 2;
}
```

Compile the example with our compiler (ACC):

``` bash
./bin/acc example.c -o example.s
```

The assembly generated is:

``` asm
	.text
	.global main
main:
	mov r0, #2
	bx lr
```

Use GCC to translate that assembly into a executable binary:

``` bash
gcc example.s -o example
```

Execute and check the result:

``` bash
$ ./example
$ echo $?
2
```

### Future

As you can see this project is going to take a long time to be completed. My plan is to work adding small features at a time. The next step is to add **conditionals (if and else)**. Afterwards, I will add **operators such as <, <=, >, >=, == and !=**. **Everytime I achieve a new goal in this project I will create a post like this one to show the feature and how it has been implemented**.
