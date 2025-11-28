import logging.handlers
from os import getenv, makedirs
from os.path import exists
from dotenv import find_dotenv, load_dotenv
from typing import Optional
import json
import logging

load_dotenv(find_dotenv())


class Log:
    def __init__(self, name: Optional[str]) -> None:
        self.debug = getenv("DEBUG")
        self.log_dir = getenv("LOG_PATH")
        self.handlers: list = []
        self.name = name
        self.logger = logging.getLogger(self.name)

    def make_log_dir(self) -> None:
        if self.log_dir:
            if not exists(path=self.log_dir):
                try:
                    makedirs(name=self.log_dir, exist_ok=True)
                except Exception as e:
                    logging.exception(f"{e}")

    def add_stream_handler(self) -> None:
        self.handlers.append(logging.StreamHandler())

    def add_file_handler(self) -> None:
        if self.name and self.log_dir:
            self.handlers.append(
                logging.handlers.RotatingFileHandler(
                    filename=f"{self.log_dir}/{self.name}.log",
                    maxBytes=int(getenv("LOG_MAX_BYTES", 1000000)),
                    backupCount=int(getenv("LOG_FILE_COUNT", 3)),
                    encoding="utf8",
                )
            )

    def basic_config(self) -> None:
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(name)s:%(funcName)s:%(lineno)d] %(message)s"
        )

        self.logger.handlers.clear()

        for handler in self.handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.propagate = False

    def get_logger(self):
        return self.logger


def log_factory(name: Optional[str]) -> logging.Logger:
    _logger_ = Log(name)
    _logger_.add_stream_handler()
    _logger_.make_log_dir()
    _logger_.add_file_handler()
    _logger_.basic_config()
    return _logger_.get_logger()

