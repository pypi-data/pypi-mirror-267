# Vellox

Vellox is an adapter for running [ASGI](https://asgi.readthedocs.io/en/latest) applications in GCP Cloud Functions.

## Requirements

Python 3.8+

## Example

```python
from vellox import Vellox

async def app(scope, receive, send):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain; charset=utf-8"]],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello, world!"})


vellox = Vellox(app=app, lifespan="off")

def handler(request):
    return vellox(request)
```

Or using a framework:

```python
from fastapi import FastAPI
from vellox import Vellox

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

vellox = Vellox(app=app, lifespan="off")

def handler(request):
    return vellox(request)
```
