import asyncio

from telegram.ext import Application


class BotRegistry:
    """
    Registry for multiple Application instances.

    Ensures each Application.initialize() is called exactly once,
    """

    def __init__(self):
        self._apps: dict[str, Application] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._initialized: set[str] = set()

    def register(self, name: str, app: Application):
        self._apps[name] = app
        self._locks[name] = asyncio.Lock()

    def get(self, name: str) -> Application:
        """
        Get bot from the regisry by name.
        """
        try:
            app = self._apps[name]
            return app
        except KeyError:
            raise ValueError(f"Bot '{name}' not found in registry.")

    def get_all(self) -> dict[str, Application]:
        return self._apps

    async def ensure_initialized(self, name: str):
        """
        Ensures each Application.initialize() is called exactly once,
        """

        # Skip if app is already initialized.
        if name in self._initialized:
            return

        async with self._locks[name]:
            if name not in self._initialized:
                await self._apps[name].initialize()
                self._initialized.add(name)


registry = BotRegistry()
