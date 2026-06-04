+++
title = "Unit test with HTTP client in Go"
date = "2026-06-04T00:00:00+00:00"
author = "Oscar Forner"
tags = ["Go"]
categories = ["Development", "Unit test", "HTTP"]
draft = false
+++

## Introduction

In this post we will explore an example of how to test code with unit test that uses an HTTP client.

## Code with HTTP Client

The following code is a typical example of a function that uses an HTTP client to do some requests.

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
)

var (
	ErrFailedToCreateRequest    = errors.New("failed to create request")
	ErrFailedToPerformRequest   = errors.New("failed to perform request")
	ErrFailedToReadBody         = errors.New("failed to read body")
	ErrStatusCodeInvalid        = errors.New("invalid status code")
	ErrBodyDoesNotContainWololo = errors.New("body does not contain wololo")
)

func GetValuesAndProcessThem(ctx context.Context, client *http.Client) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, "GET", "http://wololo:1234/", nil)
	if err != nil {
		return nil, ErrFailedToCreateRequest
	}

	res, err := client.Do(req)
	if err != nil {
		return nil, ErrFailedToPerformRequest
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		return nil, ErrStatusCodeInvalid
	}

	// Do not read the whole body at once like here. This is just to keep it short.
	body, err := io.ReadAll(res.Body)
	if err != nil {
		return nil, ErrFailedToReadBody
	}

	if !strings.Contains(string(body), "wololo") {
		return nil, ErrBodyDoesNotContainWololo
	}

	return body, nil
}
```

## Testing the code

As you probably know, the problem with testing this kind of code is having to use the package **httptest** for unit test. Or even spining a whole web server up for integration test.

Both options are valid, but sometimes you do not want to overkill it with either way mentioned before. In those cases, we can mock the **RoundTripper** for the transport attribute of the **http.Client**.

### Generate mock for RoundTripper

You can use Uber's **mockgen** to generate a mock for the **RoundTripper** with the following statement.
```go
//go:generate go tool mockgen -destination mocks/http.go -package mock net/http RoundTripper
```

And you can construct the **http.Client** like the following example:
```go
ctrl := gomock.NewController(t)
transport := mock.NewMockRoundTripper(ctrl)
client := &http.Client{Transport: transport}
```

### Example of the test

```go
package main_test

import (
	"bytes"
	"context"
	"errors"
	"io"
	"net/http"
	"testing"

	"github.com/stretchr/testify/require"
	"go.uber.org/mock/gomock"

	main "2026_go_http_unit_test"
	mock "2026_go_http_unit_test/mocks"
)

//go:generate go tool mockgen -destination mocks/http.go -package mock net/http RoundTripper
//go:generate go tool mockgen -destination mocks/io.go -package mock io Reader

func Test_getValuesAndProcessThem(t *testing.T) {
	tests := []struct {
		name      string
		ctx       context.Context
		mockSetup func(transport *mock.MockRoundTripper, reader *mock.MockReader)
		want      []byte
		wantErr   error
	}{
		{
			name: "success",
			ctx:  context.Background(),
			mockSetup: func(transport *mock.MockRoundTripper, _ *mock.MockReader) {
				transport.EXPECT().RoundTrip(gomock.Any()).Return(&http.Response{
					StatusCode: 200,
					Body:       io.NopCloser(bytes.NewBufferString("<h1>wololo</h1>")),
				}, nil)
			},
			want:    []byte("<h1>wololo</h1>"),
			wantErr: nil,
		},
		{
			name: "http request fails",
			ctx:  context.Background(),
			mockSetup: func(transport *mock.MockRoundTripper, _ *mock.MockReader) {
				transport.EXPECT().RoundTrip(gomock.Any()).Return(nil, errors.New("http request failed"))
			},
			want:    nil,
			wantErr: main.ErrFailedToPerformRequest,
		},
		{
			name: "http status code not 200",
			ctx:  context.Background(),
			mockSetup: func(transport *mock.MockRoundTripper, _ *mock.MockReader) {
				transport.EXPECT().RoundTrip(gomock.Any()).Return(&http.Response{
					StatusCode: 404,
					Body:       io.NopCloser(bytes.NewBufferString("<h1>Not found</h1>")),
				}, nil)
			},
			want:    nil,
			wantErr: main.ErrStatusCodeInvalid,
		},
		{
			name: "fails to read body",
			ctx:  context.Background(),
			mockSetup: func(transport *mock.MockRoundTripper, reader *mock.MockReader) {
				reader.EXPECT().Read(gomock.Any()).Return(0, errors.New("read body failed"))
				transport.EXPECT().RoundTrip(gomock.Any()).Return(&http.Response{
					StatusCode: 200,
					Body:       io.NopCloser(reader),
				}, nil)
			},
			want:    nil,
			wantErr: main.ErrFailedToReadBody,
		},
		{
			name: "body does not contain wololo",
			ctx:  context.Background(),
			mockSetup: func(transport *mock.MockRoundTripper, _ *mock.MockReader) {
				transport.EXPECT().RoundTrip(gomock.Any()).Return(&http.Response{
					StatusCode: 200,
					Body:       io.NopCloser(bytes.NewBufferString("<h1>try again</h1>")),
				}, nil)
			},
			want:    nil,
			wantErr: main.ErrBodyDoesNotContainWololo,
		},
		{
			name:      "ctx fails",
			ctx:       nil,
			mockSetup: func(transport *mock.MockRoundTripper, reader *mock.MockReader) {},
			want:      nil,
			wantErr:   main.ErrFailedToCreateRequest,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			transport := mock.NewMockRoundTripper(ctrl)
			reader := mock.NewMockReader(ctrl)
			tt.mockSetup(transport, reader)

			got, err := main.GetValuesAndProcessThem(tt.ctx, &http.Client{Transport: transport})

			if tt.wantErr != nil {
				require.ErrorIs(t, err, tt.wantErr)
				require.Nil(t, got)
			} else {
				require.NoError(t, err)
				require.Equal(t, tt.want, got)
			}
		})
	}
}
```

#### Execution

```bash
$ go generate ./...
go: downloading go.uber.org/mock v0.6.0
go: downloading golang.org/x/tools v0.36.0
go: downloading golang.org/x/mod v0.27.0
go: downloading golang.org/x/sync v0.16.0

$ go test ./...
go: downloading github.com/stretchr/testify v1.9.0
ok  	2026_go_http_unit_test	0.004s
?   	2026_go_http_unit_test/mocks	[no test files]
```
