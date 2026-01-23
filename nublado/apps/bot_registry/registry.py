import asyncio

from telegram.ext import Application

class BotRegistry:

    def __init__(self):
        self._apps: dict[str, Application] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._initialized: set[str] = set()

    def register(self, name: str, app: Application):
        self._apps[name] = app
        self._locks[name] = asyncio.Lock()

    def get(self, name: str) -> Application:
        return self._apps[name]

    async def ensure_initialized(self, name: str):
        # Skip if app is already initialized.
        if name in self._initialized:
            return

        async with self._locks[name]:
            if name not in self._initialized:
                await self._apps[name].initialize()
                self._initialized.add(name)


registry = BotRegistry()