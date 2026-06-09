"""Production entrypoint: `python -m server`.

Reads [server] host/port from config.toml and launches uvicorn. The systemd
unit on the Raspberry Pi uses this so config.toml is the single source of
truth for the bind address. For development keep using
`uvicorn server.main:app --reload`.
"""

import uvicorn

from server.core.config import load_config


def main() -> None:
    config = load_config()
    uvicorn.run(
        "server.main:app",
        host=config.server.host,
        port=config.server.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
