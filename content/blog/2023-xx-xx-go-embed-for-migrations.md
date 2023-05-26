+++
title = "Go embed for migrations"
date = "2023-02-03T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Go"]
categories = ["Development", "Database", "Migration"]
draft = false
+++

## What is embed?

[Go Embed](https://pkg.go.dev/embed) was introduced in [Go 1.16](https://tip.golang.org/doc/go1.16#library-embed) as a core library that allows binaries to contain external files embedded and they are accessible from inside the binary.

There are multiple way to benefit from this amazing feature, from packing your whole webapp with all its assets, to have binaries containing their DB migrations to always have the correct DB schema to interact with it.

*Note: I do not recommend to serve all webapp assets from the binary for webapps with high traffic load. Using Nginx, or a CDN would be way better.*

## Go-Migrate to run migrations

[Go-Migrate](https://github.com/golang-migrate/migrate) is a library to handle all aspects of DB migrations in Go. It is both a [CLI tool](https://github.com/golang-migrate/migrate#cli-usage), and a [library](https://github.com/golang-migrate/migrate#use-in-your-go-project).

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

## Links

* [Source Code used in this post](https://github.com/maitesin/blog/tree/master/2023_go_embed_for_migrations)
* [Embed Library Documentation](https://pkg.go.dev/embed)
* [Go 1.16 release notes](https://tip.golang.org/doc/go1.16#library-embed)
* [Go-Migrate GitHub repository](https://github.com/golang-migrate/migrate)
