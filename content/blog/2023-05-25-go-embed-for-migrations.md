+++
title = "Go embed for migrations"
date = "2023-05-25T00:00:00+00:00"
author = "Oscar Forner"
tags = ["Go"]
categories = ["Development", "Database", "Migration"]
draft = false
+++

## Introduction

In this post we will explore an example of a Go binary that combines features such as [Go Embed](https://pkg.go.dev/embed) and [Go-Migrate](https://github.com/golang-migrate/migrate) to have a self-contained binary that runs the appropriate migrations before starting any actual work.

## What is embed?

[Go Embed](https://pkg.go.dev/embed) was introduced in [Go 1.16](https://tip.golang.org/doc/go1.16#library-embed) as a core library that allows binaries to contain external files embedded and they are accessible from inside the binary.

There are multiple ways to benefit from this amazing feature, from packing your whole webapp with all its assets, to having binaries containing their DB migrations to always have the correct DB schema to interact with.

*Note: I do not recommend to serve all webapp assets from the binary for webapps with high traffic load. Using Nginx, or a CDN would be a better way to do it.*

## Go-Migrate to run migrations

[Go-Migrate](https://github.com/golang-migrate/migrate) is a library to handle all aspects of DB migrations in Go. It is both a [CLI tool](https://github.com/golang-migrate/migrate#cli-usage), and a [library](https://github.com/golang-migrate/migrate#use-in-your-go-project).

### Go-Migrate CLI tool

#### Install

```bash
$ go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
go: downloading github.com/golang-migrate/migrate v3.5.4+incompatible
go: downloading github.com/lib/pq v1.10.0
```

#### Create new migration

```bash
$ migrate create -ext sql -dir migrations -seq create_example_table
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_example_table.up.sql
/home/maitesin/dev/blog/2023_go_embed_for_migrations/migrations/000001_create_example_table.down.sql
```

## Go-Migrate with Go Embed

The following source code shows how Go-Migrate can use the embedded migrations in the binary.

```go
package main

import (
	"database/sql"
	"embed"
	"fmt"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	"github.com/golang-migrate/migrate/v4/source/iofs"
	_ "github.com/lib/pq"
)

const dbURL = "postgres://postgres:postgres@localhost:54321/examples?sslmode=disable"

//go:embed migrations/*.sql
var migrationsFS embed.FS

func main() {
	dbConn, err := sql.Open("postgres", dbURL)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer dbConn.Close()

	d, err := iofs.New(migrationsFS, "migrations")
	if err != nil {
		fmt.Println(err)
		return
	}

	migrations, err := migrate.NewWithSourceInstance("iofs", d, dbURL)
	if err != nil {
		fmt.Println(err)
		return
	}

	err = migrations.Up()
	if err != nil && err.Error() != "no change" {
		fmt.Println(err)
		return
	}

	// Here goes your awesome code to get rich :D
}
```

### Extra setup

Obviously you will need a DB - PostgreSQL in this example - to connect to in order to run the migrations. And the migration files to be placed in the correct location for the go binary to find them.

For the example used in this post we have the following filesystem hierarchy:

```bash
.
├── docker-compose.yml
├── go.mod
├── go.sum
├── main.go
└── migrations
    ├── 000001_create_examples_table.down.sql
    └── 000001_create_examples_table.up.sql
```

#### Docker for Postgres

When I am developing, I tend to work with a DB locally running inside Docker. So, for this example I have used the same approach. The following is the dockerfile that sets the PostgreSQL instance up.

Please note that there is no entry point set up for it in order to do a migration. Since the migration will be done completely from the Go binary.

```dockerfile
version: "3"

services:
  db:
    image: postgres:${POSTGRES_VERSION:-15}
    environment:
      POSTGRES_USER: ${DB_USERNAME:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-examples}
    ports:
      - "${DB_HOST:-127.0.0.1}:${DB_PORT:-54321}:5432"
    command: ["postgres", "-c", "log_statement=all"]
```

#### Migration files

The migration file to create the `examples` table is:

```sql
CREATE TABLE IF NOT EXISTS examples(
   id serial PRIMARY KEY,
   name VARCHAR (50) UNIQUE NOT NULL
);
```

The rollback file to revert the creation of the `examples` table is:

```sql
DROP TABLE IF EXISTS examples;
```

### Execution

If we put all of the above steps together, we can get an execution like the one shown in the following gif:

![](/img/blog/go_embed_db_migrations/demo.gif)

## Conclusion

As shown in this post, we can use the `embed` library and `go-migrate` tool to build binaries that can run and verify DB migrations.

This is useful in multiple scenarios, such as building binaries for sidecar pods for Kubernetes deployments, or microservices that are self-contained with the DB migrations they require to be run.

## Links

* [Source Code used in this post](https://github.com/maitesin/blog/tree/master/2023_go_embed_for_migrations)
* [Embed Library Documentation](https://pkg.go.dev/embed)
* [Go 1.16 release notes](https://tip.golang.org/doc/go1.16#library-embed)
* [Go-Migrate GitHub repository](https://github.com/golang-migrate/migrate)
