import uvicorn

from api.config import config


def main() -> None:
    uvicorn.run(
        app="api.app:app",
        host=config.app.host,
        port=config.app.port,
        reload=config.app.reload,
    )


if __name__ == "__main__":
    main()
