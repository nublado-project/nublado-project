import asyncio

from .bot import get_application

application = get_application()

_init_lock = asyncio.Lock()
_initialized = False


async def ensure_initialized():
    global _initialized

    if _initialized:
        return

    async with _init_lock:
        if not _initialized:
            await application.initialize()
            _initialized = True
