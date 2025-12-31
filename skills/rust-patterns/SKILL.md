---
name: rust-patterns
description: Rust best practices including ownership, error handling, async patterns, and idiomatic code.
---

# Rust Best Practices

## Project Structure

```
src/
├── main.rs           # Entry point (binary)
├── lib.rs            # Library root (re-exports)
├── error.rs          # Custom error types
├── config.rs         # Configuration (config crate)
├── models/           # Data structures
│   └── mod.rs
├── handlers/         # HTTP handlers (Axum/Actix)
│   └── mod.rs
├── services/         # Business logic
│   └── mod.rs
├── repository/       # Database access (SQLx/Diesel)
│   └── mod.rs
└── utils/            # Helpers
    └── mod.rs
```

## Error Handling

```rust
use thiserror::Error;

// Custom error type with thiserror
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Unauthorized")]
    Unauthorized,
}

// Result type alias
pub type Result<T> = std::result::Result<T, AppError>;

// Convert to HTTP response (Axum)
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".into()),
            AppError::Database(e) => {
                tracing::error!("Database error: {:?}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".into())
            }
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

## Ownership Patterns

```rust
// Prefer borrowing over cloning
fn process(data: &str) -> String {
    data.to_uppercase()
}

// Use Cow for flexible ownership
use std::borrow::Cow;

fn maybe_modify(s: &str, modify: bool) -> Cow<str> {
    if modify {
        Cow::Owned(s.to_uppercase())
    } else {
        Cow::Borrowed(s)
    }
}

// Builder pattern for complex structs
#[derive(Default)]
pub struct RequestBuilder {
    url: String,
    headers: Vec<(String, String)>,
    timeout: Option<Duration>,
}

impl RequestBuilder {
    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = url.into();
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push((key.into(), value.into()));
        self
    }

    pub fn timeout(mut self, duration: Duration) -> Self {
        self.timeout = Some(duration);
        self
    }

    pub fn build(self) -> Request {
        Request { /* ... */ }
    }
}
```

## Async Patterns (Tokio)

```rust
use tokio::sync::{mpsc, oneshot};

// Concurrent operations
async fn fetch_all(urls: Vec<String>) -> Vec<Result<Response>> {
    let futures: Vec<_> = urls
        .into_iter()
        .map(|url| async move {
            reqwest::get(&url).await.map_err(Into::into)
        })
        .collect();

    futures::future::join_all(futures).await
}

// Channel communication
async fn worker_pool(rx: mpsc::Receiver<Task>) {
    while let Some(task) = rx.recv().await {
        tokio::spawn(async move {
            process_task(task).await;
        });
    }
}

// Graceful shutdown
async fn run_server() {
    let (shutdown_tx, shutdown_rx) = oneshot::channel();

    tokio::spawn(async move {
        tokio::signal::ctrl_c().await.ok();
        shutdown_tx.send(()).ok();
    });

    server.with_graceful_shutdown(async {
        shutdown_rx.await.ok();
    }).await;
}
```

## Traits & Generics

```rust
// Trait for repository pattern
#[async_trait]
pub trait Repository<T> {
    async fn find_by_id(&self, id: i64) -> Result<Option<T>>;
    async fn find_all(&self) -> Result<Vec<T>>;
    async fn create(&self, item: &T) -> Result<i64>;
    async fn update(&self, item: &T) -> Result<()>;
    async fn delete(&self, id: i64) -> Result<()>;
}

// Generic function with bounds
fn process<T: Serialize + Debug>(item: T) -> Result<String> {
    tracing::debug!("Processing: {:?}", item);
    serde_json::to_string(&item).map_err(Into::into)
}

// Extension trait pattern
pub trait StringExt {
    fn truncate_safe(&self, max_len: usize) -> &str;
}

impl StringExt for str {
    fn truncate_safe(&self, max_len: usize) -> &str {
        if self.len() <= max_len {
            return self;
        }
        match self.char_indices().nth(max_len) {
            Some((idx, _)) => &self[..idx],
            None => self,
        }
    }
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Unit test
    #[test]
    fn test_validation() {
        let result = validate_email("test@example.com");
        assert!(result.is_ok());
    }

    // Async test
    #[tokio::test]
    async fn test_fetch_user() {
        let repo = MockUserRepo::new();
        let user = repo.find_by_id(1).await.unwrap();
        assert_eq!(user.name, "Test");
    }

    // Property-based testing with proptest
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn test_parse_roundtrip(s in "\\PC*") {
            let parsed = parse(&s);
            if let Ok(value) = parsed {
                assert_eq!(format!("{}", value), s);
            }
        }
    }
}
```

## Performance Tips

```rust
// Use iterators over loops
let sum: i32 = items.iter().filter(|x| x.active).map(|x| x.value).sum();

// Avoid unnecessary allocations
fn concat_strings(parts: &[&str]) -> String {
    let total_len: usize = parts.iter().map(|s| s.len()).sum();
    let mut result = String::with_capacity(total_len);
    for part in parts {
        result.push_str(part);
    }
    result
}

// Use Arc for shared ownership across threads
use std::sync::Arc;
let shared_data = Arc::new(ExpensiveData::load());
let handle = tokio::spawn({
    let data = Arc::clone(&shared_data);
    async move { process(&data).await }
});
```

## Cargo.toml Essentials

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
axum = "0.7"
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "1"
tracing = "0.1"
tracing-subscriber = "0.3"

[dev-dependencies]
tokio-test = "0.4"
proptest = "1"

[profile.release]
lto = true
codegen-units = 1
```

## Common Patterns

```rust
// Type-state pattern for compile-time safety
struct Request<State> {
    inner: RequestInner,
    _marker: PhantomData<State>,
}

struct Pending;
struct Sent;

impl Request<Pending> {
    fn send(self) -> Request<Sent> {
        // ...
    }
}

impl Request<Sent> {
    async fn response(self) -> Response {
        // ...
    }
}

// Newtype pattern for type safety
struct UserId(i64);
struct PostId(i64);

fn get_user(id: UserId) -> User { /* ... */ }
// get_user(PostId(1)) won't compile!
```
