# On Windows, temporary file shold delete "after" storage was deleted
# NamedTemporaryFilePool ensures tempfile delete after tests.

from __future__ import annotations

import atexit
import os
import tempfile
from types import TracebackType
from typing import Any
from typing import IO
from typing import List
from typing import Type


class NamedTemporaryFilePool:
    tempfile_pool: List[IO[Any]] = []

    def __new__(cls, **kwargs: Any) -> "NamedTemporaryFilePool":
        if not hasattr(cls, "_instance"):
            cls._instance = super(NamedTemporaryFilePool, cls).__new__(cls)
            atexit.register(cls._instance.cleanup)
        return cls._instance

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def tempfile(self) -> IO[Any]:
        tmpfile = tempfile.NamedTemporaryFile(delete=False, **self.kwargs)
        self.tempfile_pool.append(tmpfile)
        return tmpfile

    def cleanup(self) -> None:
        for i in self.tempfile_pool:
            os.unlink(i.name)

    def __enter__(self) -> IO[Any]:
        return self.tempfile()

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        pass
