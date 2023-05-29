+++
title = "No Naked Boolean Parameters"
date = "2020-04-18T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Pattern", "Dessign"]
categories = ["Development"]
+++

## Introduction

**We all have used naked boolean parameters at some point during our lives**, specially when we were starting to learn to program. Other times we add them when refactoring code, or we are just hacking somthing together. However, **naked boolean parameters are a code smell and signs of a bad code**.

First, **they hurt the readability of the code** and since we spend the vast majority of our time reading code, that is a big reason to avoid naked boolean parameters. Okay... some IDEs add nice information like the name of the parameters passed, but you do not have that when you are doing code reviews :D

Second, **naked boolean parameters can be confusing when several of them are present in the same parameter list**. Specially, if they are all together one after the other.

```go
func openRemoteFile(url string, allowRetries, allowRedirects bool) {
	if allowRetries {
		fmt.Println("Redirects enabled")
	}
	if allowRedirects {
		fmt.Println("Retries enabled")
	}
}
```

When calling that method you will see something like the following

```go
openRemoteFile("sftp://myserver.com/wololo.txt", true, false)
```

As you can see, **the first thing you will have to do upon reading this code is to go to the definition of the function**, just to know which parameter is being passed as true and which one is being passed as false.

## Wrapper functions

One way to improve the readability of the function is to create **wrapper functions that set specific values for the boolean parameters**. This is useful if these **wrapper functions are the public way to call the non-shared function that contains the naked boolean parameters**.

```go
func OpenRemoteFile(url string) {
    openRemoteFile(url, false, false)
}

func OpenRemoteFileWithRetries(url string) {
    openRemoteFile(url, true, false)
}

func OpenRemoteFileWithRedirects(url string) {
    openRemoteFile(url, false, true)
}

func OpenRemoteFileWithRetriesAndRedirects(url string) {
    openRemoteFile(url, true, true)
}
```

As you can imagine, the amount of these wrapper functions grows exponentially based on the number of boolean parameters. **This option is only viable if the number of boolean parameters is low and the possible viable combinations of them are small**.

## Named booleans

Another way to improve the readability of the function is to use named booleans.

```go
const (
	allowRetries = true
	disallowRetries = false
	allowRedirects = true
	disallowRedirects = false
)
```

Now, the call to `openRemoteFile` will look something like this.

```go
openRemoteFile("sftp://myserver.com/wololo.txt", allowRetries, disallowRedirects)
```

The main problem with this solution is that **it only fixes the readability issue, but the problem of mixing the boolean parameters order still in place**.

This is a totally valid code, but **it does not do what you would expect by reading the parameters**.

```go
openRemoteFile("sftp://myserver.com/wololo.txt", allowRedirects, disallowRetries)
```

## Bitmask

Bitmask is only an option if **all the possible combinations of the boolean parameters are viable. Being viable means that all the combinations make sense**.

```go
type RemoteMark uint8

const (
    Redirects RemoteMark = 1 << iota
    Retries
)

func openRemoteFile(url string, mask RemoteMark) {
	if mask & Redirects == Redirects {
		fmt.Println("Redirects enabled")
	}
	if mask & Retries == Retries {
		fmt.Println("Retries enabled")
	}
}
```

If the `openRemoteFile` function signature is changed to match the one above, then it can be called like

```go
openRemoteFile("sftp://myserver.com/wololo.txt", Redirects | Retries)
```

**This solution is both more readable and less error prone**. It avoids the usage of multiple boolean parameters, however, this approach case can only be used if **all the combinations of values of the boolean parameters are viable**.

## Typed booleans

Last, but not least, *typed booleans*. You can think of *typed booleans* as an improvement over *named booleans*. This is because ***typed booleans*** **not only solve the readability problem**, like *names booleans*, **but they solve the problem of mixing the order of the boolean parameters as well**.

```go
type RedirectEnum bool
type RetryEnum bool

const (
	DisallowRedirects RedirectEnum = false
	AllowRedirects

	DisallowRetries RetryEnum = false
	AllowRetries
)

func openRemoteFile(url string, redirects RedirectEnum, retries RetryEnum) {
	if redirects == AllowRedirects {
		fmt.Println("Redirects enabled")
	}
	if retries == AllowRetries {
		fmt.Println("Retries enabled")
	}
}
```

If the `openRemoteFile` function signature is changed to match the one above, then it can be called like

```go
openRemoteFile("sftp://myserver.com/wololo.txt", AllowRedirects, DisallowRetries)
```

The snippet above shows code that is correct and readable. In addition, if you mix the order like in the following example

```go
openRemoteFile("sftp://myserver.com/wololo.txt", DisallowRetries, AllowRedirects)
```

When compiling it, an error similar to the following would be displayed

```bash
./prog.go:29:17: cannot use DisallowRetries (type RetryEnum) as type RedirectEnum in argument to openRemoteFile
./prog.go:29:17: cannot use AllowRedirects (type RedirectEnum) as type RetryEnum in argument to openRemoteFile
```

## Conclusion

**Writing readable code is one of the most important parts of software development**, as we spend way more time reading code than writing it. Therefore, **if you make the effort to use the patterns described above the readability of your code base will increase**.

**I strongly recommend the usage of *typed booleans* and *bitmasks* when possible**. They do not only improve the readability of the code, but they also improve the correctness of the code.
