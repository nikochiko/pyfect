# Pyfect

Pyfect implements a simple effect handling
prototype in Python.

[`example.py`](/example.py) implements a simple
version where we use `Print` and a `Square`
effects. This is of no practical significance
and I would like ideas for better examples.

## Usage

```python
# Create an effect by subclassing `Effect`
from pyfect import Effect

class Increment(Effect):
    # each effect can have its own arbitrary __init__
    def __init__(self, value: int):
        self.value = value

# Create a handler for this
from pyfect import Continuation

def increment_handler[T](effect: Square, continuation: Continuation[T]) -> T:
    # you can pass values to the continuation
    return continuation(effect.value + 1)

# Create a runner and register handlers
from pyfect import Runner

runner = Runner()
runner.register(Fork, fork_handler)

# Write an entrypoint function and call runner.run with it
def main():
    x, y = 1, 10
    x1 = yield Increment(x)
    y1 = yield Increment(y)
    print(f"incremented {x1=} {y1=}")

    # values can be returned normally
    return 1
```

The way to write and call functions now changes.
Any effect should be yielded. All subroutines that
use effects should be generators. Function calling
for these subroutines would change to `yield from`.

