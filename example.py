from __future__ import annotations

import logging
from pyfect import Continuation, Effect, Execution, Runner


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Print(Effect):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def handler[T](eff: Print, continuation: Continuation[T]) -> T:
        logger.info("Print effect handled")
        print(*eff.args, **eff.kwargs)
        return continuation()


class Square(Effect):
    def __init__(self, x: int):
        self.x = x

    @staticmethod
    def handler[T](eff: Square, continuation: Continuation[T]):
        result = eff.x * eff.x
        logger.info(f"Square effect handled: {eff.x} -> {result}")
        return continuation(result)


# ---


def subroutine():
    yield Print("Inside the subroutine")


def program() -> Execution[int]:
    yield Print("Hello, World!")
    four = yield Square(2)
    yield from subroutine()
    yield Print("The square of 2 is", four)
    return 5


if __name__ == "__main__":
    runner = Runner()
    runner.register(Print, Print.handler)
    runner.register(Square, Square.handler)

    handler_names = [cls.__name__ for cls in runner.handlers]
    logger.info(f"Running program with effects: {handler_names}")
    result = runner.run(program)
    logger.info(f"Program ended with result: {result}")

