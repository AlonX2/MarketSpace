import threading

from typing import Any

class CallFutureException(Exception):
    pass

class CallFuture:
    def __init__(self) -> None:
        self.result: Any = None
        self.error: Exception | None = None
        self.happened = threading.Event()

    def set_result(self, result: Any):
        if self.happened.is_set():
            raise CallFutureException("Cannot set result of call_future after a result or an error was already set")
        self.result = result
        self.happened.set()

    def set_error(self, error: Exception):
        if self.happened.is_set():
            raise CallFutureException("Cannot set error of call_future after a result or an error was already set")
        self.error = error
        self.happened.set()