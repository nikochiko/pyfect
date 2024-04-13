from typing import Any, Callable, Generator


class Effect():
    ...


type Continuation[T] = Callable[..., T]
type EffectHandler[E: Effect, T] = Callable[[E, Continuation[T]], T]

type Execution[T] = Generator[Effect, Any, T]
type Effectful[T] = Callable[..., Execution[T]]


class Runner:
    def __init__(self):
        self.handlers: dict[type[Effect], EffectHandler] = {}

    def register[E: Effect, T](self, effect_t: type[Effect], handler: EffectHandler[E, T]):
        self.handlers[effect_t] = handler

    def run[T](self, fn: Effectful[T]) -> T:
        return self._run(fn(), None)

    def _run[T](self, execution: Execution[T], arg: Any) -> T:
        try:
            eff = execution.send(arg)
        except StopIteration as e:
            return e.value

        try:
            handler = self.handlers[type(eff)]
        except KeyError:
            raise RuntimeError(f"Effect {type(eff)} not handled")

        continuation = self._make_continuation(execution)
        return handler(eff, continuation)

    def _make_continuation[T](self, execution: Execution[T]) -> Continuation[T]:
        def continuation(arg=None) -> T:
            return self._run(execution, arg)
        return continuation

