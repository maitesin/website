+++
title = "ARM C Compiler (ACC): basic compiler II"
date = "2015-06-24T13:50:46+02:00"
author = "Oscar Forner"
tags = [""]
categories = ["Development"]
+++

### Table of Contents
[TOC]

### Introduction
I am working on a pet project to create a **C compiler for the ARM architecture**. You can find more information about this topic in my previous post [ARM C Compiler (ACC) - Basic Compiler I](http://maitesin.github.io//ARM-C-Compiler_ACC_basic_compiler/).

The source code of this project can be found in [GitHub](https://github.com/maitesin/acc).

### What is the current state of the project?
Currently, I have implemented a **very basic compiler**, this version is available in [GitHub as v0.2](https://github.com/maitesin/acc/tree/v0.2). *Basic compiler able to handle a single file with a main function (without parameters) and if/else statements with simple boolean expressions and return statements of a positive integer*.

#### What has been added or modified since the last post?
The difference between both versions can be found in the following link [diff v0.1 v0.2](https://github.com/maitesin/acc/compare/v0.1...v0.2).

##### Unit tests
In the previous version only **unit tests** were available for the **Lexer**, but in this new version some **unit tests** for the **Lexer** have been added and **unit tests** for the **Grammar** have been created. In total, **there are 27 (26 new) unit tests for Lexer and 12 unit tests for Grammar**.

##### Lexer and Tokens
There are new **Tokens** for **if**, **else** and **boolean operators**. **Lexer** now supports all these new tokens and it has a new feature (a **stack**) that allows the **Grammar** to give a **Token** back to **Lexer**. **That is useful when you are reading a boolean expression, but you do not know if it will be a binary or unary expression**. Then in case you try to check if it is a binary expression and it is not, you give back that token to the **Lexer** and try with the unary expression. Moreover, the **Lexer** now receives a buffer with the content of the file loaded instead of a file. This is to make it easier to create **unit tests**.
``` c
void init_lexer(lexer * l, char * code)
{
	l->f = code;
	l->stack = NULL;
	l->count = 0;
}

void destroy_lexer(lexer * l)
{
	stack_base * tmp = NULL;
	stack_base * s = l->stack;
	if (s != NULL)
	{
		tmp = s;
		s = s->next;
		free_stack_base(tmp);
	}
}

void free_stack_base(stack_base * s)
{
	free(s);
}

void push_back(lexer * l, token_base * t)
{
	stack_base * s = (stack_base *) malloc(sizeof(stack_base));
	s->token = t;
	s->next = l->stack;
	l->stack = s;
}

char get_char(lexer * l)
{
	return l->f[l->count++];
}

void push_back_chars(lexer * l, size_t amount)
{
	if (l->count >= amount)
	{
		l->count -= amount;
	}
	else
	{
		fprintf(stderr, "Error moving back in the buffer\n");
		exit(EXIT_FAILURE);
	}
}

void push_back_one_char(lexer * l)
{
	push_back_chars(l, 1);
}

struct token_base * next(lexer * l)
{
	char buffer[512];
	char * buff_copy = NULL;
	int pos = 0;
	size_t state = 0;
	char tmp;
	void * result = NULL;
	stack_base * stack = NULL;

	if (l->stack != NULL)
	{
		stack_base * stack = l->stack;
		l->stack = l->stack->next;
		result = stack->token;
		stack->token = NULL;
		free_stack_base(stack);
		return result;
	}
...
```

##### Grammar and AST nodes
The most important features added to the **AST** is the addition of **node_if**, **node_boolean_operator** and **enum boolean_operator_type**. In addition to this, now the base of the **AST** holds a pointer to the next **AST** node. **That is to hold the whole information contained in the body of a function or an if statement**.
``` c
// Boolean operators
enum boolean_operator_type {
	B_EQUALEQUAL,
	B_NOTEQUAL,
	B_LTEQUAL,
	B_GTEQUAL,
	B_OROR,
	B_ANDAND,
	B_LT,
	B_GT,
	B_NOT
};

typedef struct node_if
{
	ast_base base;
	ast_base * expression;
	ast_base * i_body;
	ast_base * e_body;
} node_if;

typedef struct node_boolean_operator
{
	ast_base base;
	ast_base * first;
	ast_base * second;
	enum boolean_operator_type oper;
} node_boolean_operator;

/*
 * Init functions for the AST nodes
 */
void init_ast_base(ast_base * base, enum ast_type type, ast_base * next);
void init_ast_base_single(ast_base * base, enum ast_type type);
void init_node_id(node_id * node, char * value);
void init_node_int(node_int * node, int value);
void init_node_function(node_function * node, char * name,
			ast_base * entry_point);
void init_node_return(node_return * node, ast_base * value);
void init_node_if(node_if * node, ast_base * expression, ast_base * i_body,
		  ast_base * e_body);
void init_node_boolean_operator(node_boolean_operator * node,
				enum boolean_operator_type type,
ast_base * first, ast_base * second);
```
Regarding the **Grammar**, the method **read_function_body** has been refactored into the method **read_body** to be able to re-use it to read the body of the **if** and **else** statements. Another interesting piece of code is the method **read_boolean_expression**, it allows to build a valid **AST** for a complex boolean expression such as *1 <= 2 && 4 == 4*.
``` c
/*
 * Read functions to build AST parts
 */
ast_base * read_function_ast_node(grammar * g);
ast_base * read_body(grammar * g);
ast_base * read_return_expression(grammar * g);
ast_base * read_if_statement(grammar * g);
ast_base * read_boolean_expression(grammar * g);
ast_base * read_single_boolean_expression(grammar * g, ast_base * r,
					  int * op_found,
					  enum boolean_operator_type op);
ast_base * read_boolean_binary_expression(grammar * g);
ast_base * read_boolean_unary_expression(grammar * g);

ast_base * read_boolean_expression(grammar * g)
{
	ast_base * root = NULL;
	token_base * token = NULL;
	enum boolean_operator_type op;
	int op_found = 0;

	token = next(g->l);
	while (token->type != T_CPAR)
	{
		switch (token->type)
		{
			case T_INT_VALUE:
				push_back(g->l, token);
				root = read_single_boolean_expression(g, root, &op_found, op);
				break;
			case T_BOOLEAN_OP:
				op = get_boolean_op_value((token_boolean_op *)token);
				op_found = 1;
				break;
			case T_OPAR:
				root = read_single_boolean_expression(g, root, &op_found, op);
				break;
			default:
				fprintf(stderr, "Error reading boolean expression\n");
				exit(EXIT_FAILURE);
		}
		token = next(g->l);
	}
	free_token_cpar((token_cpar *)token);
	return root;
}
```

##### Assembly Generator
The **Generator** of the ARM assembly has new methods to handle all the new **AST** structures and behaviours. **It has some limitations regarding boolean expressions in which I have to do further research**. Some pieces of the **Generator** are the following:
``` c
void __generate_code_for_if(generator * g, node_if * ast);
void __generate_code_for_if_expression(generator * g, ast_base * ast,
				       unsigned long long int if_num);
void __generate_code_for_binary_boolean_expression(generator * g,
					node_boolean_operator * op,
					unsigned long long int if_num);
void __generate_code_for_unary_boolean_expression(generator * g,
					node_boolean_operator * op,
					unsigned long long int if_num);
void __generate_code_for_body(generator * g, ast_base * body);

void __generate_code_for_if(generator * g, node_if * ast)
{
    unsigned long long int if_num = g->if_num;
    g->if_num++;
    // Expression
    __generate_code_for_if_expression(g, ast->expression, if_num);
    // If body
    __generate_code_for_body(g, ast->i_body);
	fprintf(g->f, "if_else_%llu:\n", if_num);
    if (ast->e_body != NULL)
    {
        // Else body
        __generate_code_for_body(g, ast->e_body);
    }
}
```

### Example of the current functionality:
The code to be compiled into ARM assembly is:
``` c
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
Compile the example with our compiler (ACC):
``` bash
./bin/acc example.c -o example.s
```
The assembly generated is:
``` asm
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
The next step will be to actually be able to generate any possible boolean expression. Currently, the **AST** can recognise complex boolean expressions, but the **Generator** is not able to handle them. I have to study and research more about this topic in the **ARM** architecture. After that, **I plan on adding variables (integers)**.
