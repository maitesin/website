+++
title = "Go embed for migrations"
date = "2023-02-03T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Go"]
categories = ["Development", "Database", "Migration"]
draft = true
+++

## What is embed?

[Go Embed](https://pkg.go.dev/embed) was introduced in [Go 1.16](https://tip.golang.org/doc/go1.16#library-embed) as a core library that allows binaries to contain external files embedded and they are accessible from inside the binary.

There are multiple way to benefit from this amazing feature, from packing your whole webapp with all its assets, to have binaries containing their DB migrations to always have the correct DB schema to interact with it.

In this post we will focus on the later case and use it as an example to explain the Go Embed feature.

## Go-Migrate to run migrations

[Go-Migrate](https://github.com/golang-migrate/migrate) is a library to handle all aspects of DB migrations in Go. It is both a [CLI tool](https://github.com/golang-migrate/migrate#cli-usage), and a [library](https://github.com/golang-migrate/migrate#use-in-your-go-project).

### Installing Go-Migrate CLI

```bash
$ go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
go: downloading github.com/golang-migrate/migrate v3.5.4+incompatible
go: downloading github.com/lib/pq v1.10.0
```

### Create new migration

```bash
$ migrate create -ext sql -dir migrations -seq create_examples_table
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_examples_table.up.sql
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_examples_table.down.sql
```

## Putting it all together


