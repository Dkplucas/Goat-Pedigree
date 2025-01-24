import os
from django.core.asgi import get_asgi_application
from asgiref.compatibility import guarantee_single_callable

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goat_pedigree.settings')

# Wrap the ASGI application with lifespan middleware
class LifespanMiddleware:
    def __init__(self, app):
        self.app = guarantee_single_callable(app)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        else:
            await self.app(scope, receive, send)

# Get the Django ASGI application
django_application = get_asgi_application()

# Wrap it with the lifespan middleware
application = LifespanMiddleware(django_application)