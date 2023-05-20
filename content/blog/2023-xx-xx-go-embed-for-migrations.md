+++
title = "Getting started with Go"
date = "2021-07-03T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Go"]
categories = ["Development"]
draft = true
+++

```bash
go mod init github.com/maitesin/example
```

```bash
$ go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
go: downloading github.com/golang-migrate/migrate v3.5.4+incompatible
go: downloading github.com/lib/pq v1.10.0
```

```bash
$ migrate create -ext sql -dir migrations -seq create_example_table
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_example_table.up.sql
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_example_table.down.sql
```
