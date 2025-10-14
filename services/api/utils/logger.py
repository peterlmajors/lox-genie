import logging
from typing import Optional

class LoxLogger:
    def __init__(self, name: Optional[str] = None, level: int = logging.INFO):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self.logger.error(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self.logger.warning(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self.logger.critical(message, *args, **kwargs)

# Export a default logger instance for convenience
logger = LoxLogger().logger