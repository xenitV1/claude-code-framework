---
name: go-patterns
description: Go best practices including error handling, concurrency, project structure, and idiomatic code.
---

# Go Best Practices

## Project Structure

```
project/
├── cmd/
│   └── server/
│       └── main.go       # Entry point
├── internal/             # Private packages
│   ├── config/
│   │   └── config.go
│   ├── handler/
│   │   └── handler.go
│   ├── service/
│   │   └── service.go
│   ├── repository/
│   │   └── repository.go
│   └── model/
│       └── model.go
├── pkg/                  # Public packages
│   └── validator/
├── api/                  # OpenAPI specs
├── migrations/           # SQL migrations
├── go.mod
└── go.sum
```

## Error Handling

```go
import (
    "errors"
    "fmt"
)

// Custom error types
type AppError struct {
    Code    string
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %s: %v", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrValidation   = errors.New("validation error")
)

// Error wrapping
func GetUser(id int64) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}

// Error checking
if errors.Is(err, ErrNotFound) {
    // Handle not found
}

var appErr *AppError
if errors.As(err, &appErr) {
    // Handle app error
}
```

## Concurrency Patterns

```go
import (
    "context"
    "sync"
    "golang.org/x/sync/errgroup"
)

// Worker pool pattern
func processItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    sem := make(chan struct{}, 10) // Limit concurrency

    for _, item := range items {
        item := item // Capture loop variable
        g.Go(func() error {
            select {
            case sem <- struct{}{}:
                defer func() { <-sem }()
            case <-ctx.Done():
                return ctx.Err()
            }
            return processItem(ctx, item)
        })
    }

    return g.Wait()
}

// Fan-out, fan-in
func fanOutFanIn(ctx context.Context, input <-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    // Fan-out to workers
    workers := 5
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for n := range input {
                select {
                case out <- process(n):
                case <-ctx.Done():
                    return
                }
            }
        }()
    }

    // Fan-in: close output when all workers done
    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

// Graceful shutdown
func runServer(ctx context.Context) error {
    srv := &http.Server{Addr: ":8080", Handler: handler}

    go func() {
        <-ctx.Done()
        shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()
        srv.Shutdown(shutdownCtx)
    }()

    return srv.ListenAndServe()
}
```

## Interfaces

```go
// Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Interface composition
type ReadWriter interface {
    Reader
    Writer
}

// Repository pattern
type UserRepository interface {
    FindByID(ctx context.Context, id int64) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}

// Accept interfaces, return structs
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

## Testing

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// Table-driven tests
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "test@example.com", false},
        {"missing @", "testexample.com", true},
        {"empty string", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}

// Mock with interface
type mockUserRepo struct {
    users map[int64]*User
}

func (m *mockUserRepo) FindByID(ctx context.Context, id int64) (*User, error) {
    if user, ok := m.users[id]; ok {
        return user, nil
    }
    return nil, ErrNotFound
}

// Integration test
func TestAPI_CreateUser(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test")
    }

    srv := setupTestServer(t)
    defer srv.Close()

    resp, err := http.Post(srv.URL+"/users", "application/json", body)
    require.NoError(t, err)
    assert.Equal(t, http.StatusCreated, resp.StatusCode)
}
```

## HTTP Handlers

```go
import (
    "encoding/json"
    "net/http"
)

// Handler with dependency injection
type Handler struct {
    userService *UserService
    logger      *slog.Logger
}

func NewHandler(us *UserService, logger *slog.Logger) *Handler {
    return &Handler{userService: us, logger: logger}
}

// Handler method
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    id := chi.URLParam(r, "id")

    userID, err := strconv.ParseInt(id, 10, 64)
    if err != nil {
        h.respondError(w, http.StatusBadRequest, "invalid user ID")
        return
    }

    user, err := h.userService.GetByID(ctx, userID)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            h.respondError(w, http.StatusNotFound, "user not found")
            return
        }
        h.logger.Error("get user", "error", err)
        h.respondError(w, http.StatusInternalServerError, "internal error")
        return
    }

    h.respondJSON(w, http.StatusOK, user)
}

// Response helpers
func (h *Handler) respondJSON(w http.ResponseWriter, status int, data any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}

func (h *Handler) respondError(w http.ResponseWriter, status int, message string) {
    h.respondJSON(w, status, map[string]string{"error": message})
}
```

## Configuration

```go
import (
    "os"
    "github.com/caarlos0/env/v9"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
}

type ServerConfig struct {
    Port         int           `env:"PORT" envDefault:"8080"`
    ReadTimeout  time.Duration `env:"READ_TIMEOUT" envDefault:"5s"`
    WriteTimeout time.Duration `env:"WRITE_TIMEOUT" envDefault:"10s"`
}

type DatabaseConfig struct {
    URL          string `env:"DATABASE_URL,required"`
    MaxOpenConns int    `env:"DB_MAX_OPEN_CONNS" envDefault:"25"`
    MaxIdleConns int    `env:"DB_MAX_IDLE_CONNS" envDefault:"5"`
}

func LoadConfig() (*Config, error) {
    var cfg Config
    if err := env.Parse(&cfg); err != nil {
        return nil, fmt.Errorf("parse config: %w", err)
    }
    return &cfg, nil
}
```

## Logging (slog)

```go
import "log/slog"

// Structured logging
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

// With context
logger.Info("user created",
    slog.Int64("user_id", user.ID),
    slog.String("email", user.Email),
    slog.Duration("duration", time.Since(start)),
)

// Add to context
ctx = context.WithValue(ctx, loggerKey, logger.With(
    slog.String("request_id", requestID),
))

// Retrieve from context
func loggerFromContext(ctx context.Context) *slog.Logger {
    if logger, ok := ctx.Value(loggerKey).(*slog.Logger); ok {
        return logger
    }
    return slog.Default()
}
```

## Common Patterns

```go
// Functional options
type ServerOption func(*Server)

func WithPort(port int) ServerOption {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(opts ...ServerOption) *Server {
    s := &Server{port: 8080, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

## go.mod Essentials

```go
module github.com/user/project

go 1.22

require (
    github.com/go-chi/chi/v5 v5.0.12
    github.com/jackc/pgx/v5 v5.5.4
    github.com/caarlos0/env/v9 v9.0.0
    golang.org/x/sync v0.6.0
)
```
