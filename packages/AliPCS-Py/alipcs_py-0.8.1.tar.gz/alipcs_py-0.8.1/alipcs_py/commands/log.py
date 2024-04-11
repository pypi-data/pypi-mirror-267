from typing import cast
import os
from pathlib import Path

from alipcs_py.common.log import LogLevels, TLogLevel, get_logger as _get_logger
from alipcs_py.commands.env import LOG_LEVEL, LOG_PATH


def get_logger(name: str):
    _LOG_PATH = Path(os.getenv("LOG_PATH") or LOG_PATH).expanduser()
    _LOG_LEVEL: TLogLevel = cast(
        TLogLevel,
        os.getenv("LOG_LEVEL", LOG_LEVEL).upper(),
    )

    assert _LOG_LEVEL in LogLevels

    return _get_logger(name, filename=_LOG_PATH, level=_LOG_LEVEL)
