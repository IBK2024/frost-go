import uvicorn
import asyncio
from run import app


async def main() -> None:
    config = uvicorn.Config(app, port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
