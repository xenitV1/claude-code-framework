---
name: python-patterns
description: Python best practices including type hints, async patterns, decorators, and project structure.
---

# Python Patterns

## Type Hints

```python
from typing import Optional, List, Dict, Callable

def get_user(user_id: int) -> Optional[User]:
    """Get user by ID, returns None if not found."""
    return db.query(User).filter(User.id == user_id).first()

def process_items(items: List[str]) -> Dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items}
```

## Async Patterns

```python
import asyncio
from typing import List

async def fetch_all(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## Decorators

```python
import functools
import time

def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def retry(max_attempts: int = 3):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
            return None
        return wrapper
    return decorator
```

## Pydantic Models

```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int

    @validator("age")
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Invalid age")
        return v
```

## Project Structure

```
src/
├── __init__.py
├── main.py
├── models/
├── services/
├── routes/
└── utils/
tests/
├── test_services.py
└── conftest.py
```
