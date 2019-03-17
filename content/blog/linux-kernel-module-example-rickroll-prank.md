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
**NOTE: The code used to replace the user's path with the one provided is BAD, never change user's pointer content unless he/she is expecting that to happen. Don't do that at home kids**

I decided to explain the basics of a **Linux Kernel Module** with humor. I am not saying this is a good idea for April's fool, but it is quite close ;)

This module shares some ideas with the post about [LD_PRELOAD](http://maitesin.github.io//LD_PRELOAD_as_defense/), but this time it is not to defend ourselves. **The module will replace the open syscall for our own where it will detect if we are opening an mp3 or a jpg file**. This idea was taken from [this talk of Julia Evans](https://www.youtube.com/watch?v=0IQlpFWTFbM).

As always, **all the code used in this post is available in this [repo](https://github.com/maitesin/blog/tree/master/rickroll_module_2016_03_19)**.

### Skeleton of a Linux Kernel Module
The following code is the skeleton of a **Linux Kernel Module**
``` c
#include<linux/module.h>
#include<linux/init.h>

MODULE_AUTHOR("Oscar Forner Martinez");
MODULE_LICENSE("GPL v2");

static int __init my_init(void)
{
  pr_info("This will be shown when the module is loaded\n");
  return 0;
}

static void __exit my_exit(void)
{
  pr_info("This will be shown when the module is removed\n");
}

module_init(my_init);
module_exit(my_exit);
```

I think the code above is quite self-explanatory.

### What does this Module do?
As said before, this module is aimed to replace the current open syscall by ours, that will detect if the file we are trying to open is an mp3 or a jpg file and it will substitute the files by the ones provided when the module is loaded.

#### Code explained
This could seem a bit overwhelming, but let's go through it.
``` c
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/init.h>
#include <linux/kallsyms.h>
#include <asm/unistd.h>
#include <linux/uaccess.h>

MODULE_AUTHOR("Oscar Forner Martinez");
MODULE_LICENSE("GPL v2");
MODULE_DESCRIPTION("This module's aim is to replace the open syscall to our own open syscall. Our own open syscall will replace the opening of all *.mp3 files by the file provided as a parameter (song). Moreover it will replace all *.jpg files by the file provided as a parameter (pict).");

static char *song = NULL;
static char *pict = NULL;

module_param(song, charp, 0000);
MODULE_PARM_DESC(song, "Path to the song to open always.");

module_param(pict, charp, 0000);
MODULE_PARM_DESC(pict, "Path to the picture to open always.");

static void **sys_call_table = NULL;

static asmlinkage long (*old_open) (const char __user *filename, int flags, umode_t mode);

static asmlinkage long rick_open(const char __user *filename, int flags, umode_t mode)
{
        size_t len = strlen(filename);
        const char *ext = filename + len - 4;
        if (strncmp(ext, ".mp3", 4) == 0 && song != NULL)
        {
                copy_to_user((void *)filename, song, len);
        }
        if (strncmp(ext, ".jpg", 4) == 0 && pict != NULL)
        {
                copy_to_user((void *)filename, pict, len);
        }
        pr_info("Let's play!\n");
        return old_open(filename, flags, mode);
}

static int __init set_rick(void)
{
        if (song == NULL && pict == NULL)
        {
                pr_info("Rickroll module not loaded. You need to provide a song and/or a picture as a parameter\n");
                return -1;
        }
        sys_call_table = (void **)kallsyms_lookup_name("sys_call_table");
        pr_info("Found sys_call_table at %p\n", sys_call_table);
        old_open = sys_call_table[__NR_open];
        sys_call_table[__NR_open] = rick_open;
        pr_info("Old open: %p; Rick open: %p\n", old_open, rick_open);
        return 0;
}

static void __exit unset_rick(void)
{
        pr_info("Party is over :(\n");
        sys_call_table[__NR_open] = old_open;
}

module_init(set_rick);
module_exit(unset_rick);
```

Parameters provided to the module are declared and registered as follows:
``` c
static char *song = NULL;
static char *pict = NULL;

module_param(song, charp, 0000);
MODULE_PARM_DESC(song, "Path to the song to open always.");

module_param(pict, charp, 0000);
MODULE_PARM_DESC(pict, "Path to the picture to open always.");
```

Pointer to the old syscall and declaration of the new one. Moreover, we can see the method ***copy_to_user***, this is to copy information from the **Kernel Space** to **User Space**.
``` c
static asmlinkage long (*old_open) (const char __user *filename, int flags, umode_t mode);

static asmlinkage long rick_open(const char __user *filename, int flags, umode_t mode)
{
        size_t len = strlen(filename);
        const char *ext = filename + len - 4;
        if (strncmp(ext, ".mp3", 4) == 0 && song != NULL)
        {
                copy_to_user((void *)filename, song, len);
        }
        if (strncmp(ext, ".jpg", 4) == 0 && pict != NULL)
        {
                copy_to_user((void *)filename, pict, len);
        }
        pr_info("Let's play!\n");
        return old_open(filename, flags, mode);
}
```

The most outstanding part of the following piece of code is the use of ***kallsyms_lookup_name*** function. We will use it to locate the address of the ***sys_call_table***.
``` c
static int __init set_rick(void)
{
        if (song == NULL && pict == NULL)
        {
                pr_info("Rickroll module not loaded. You need to provide a song and/or a picture as a parameter\n");
                return -1;
        }
        sys_call_table = (void **)kallsyms_lookup_name("sys_call_table");
        pr_info("Found sys_call_table at %p\n", sys_call_table);
        old_open = sys_call_table[__NR_open];
        sys_call_table[__NR_open] = rick_open;
        pr_info("Old open: %p; Rick open: %p\n", old_open, rick_open);
        return 0;
}

static void __exit unset_rick(void)
{
        pr_info("Party is over :(\n");
        sys_call_table[__NR_open] = old_open;
}
```

**Note: the *sys_call_table* is in read-only mode by default. To be able to write on it, the kernel running must have been compiled with the flag *CONFIG_DEBUG_RODATA* not set.**

### Example of how it works
<iframe width="560" height="315" src="https://www.youtube.com/embed/efEZZZf_nTc" frameborder="0" allowfullscreen></iframe>

### Conclusion
This is a great and funny example of the power of the **Linux Kernel Modules**. I will write about more advanced examples in the future. Moreover, I will keep on trying to get a patch accepted in the main tree :D
