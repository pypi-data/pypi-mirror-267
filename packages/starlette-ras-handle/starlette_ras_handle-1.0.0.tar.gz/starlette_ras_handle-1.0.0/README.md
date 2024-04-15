# Starlette RAS-handler
This library adds the ability to handle `RuntimeError: Caught handled exception, but response already started.` error, so you can silent it, or do whatever you want

## Usage
1. Define an async function that accepts `(Exception, Request | WebSocket)` and returns `None`
    ```python
    async def print_handler(exc: Exception, request: Request | WebSocket) -> None:
        print("Caught", exc)
    ```

2. Patch!
    ```python
    from handler import print_handler
    
    from starlette_ras_handle import handle_starlette_ras
    handle_starlette_ras(print_handler)
    
    # other imports...
    ```
   
**IMPORTANT:** If you want the patch to work properly, you should use it before you import anything, related to `starlette` (e.g. `FastAPI`)

You can check out an example in `/examples/example.py`