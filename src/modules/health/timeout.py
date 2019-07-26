import threading
from typing import Callable, Any


def timeout(func: Callable[[Any], Any], args: tuple = None, kwargs: dict = None, timeout: int = 3, default: Any = None):
    """Call function with timeout"""

    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                if default is not None:
                    self.result = default
                else:
                    self.result = e

    args = args or ()
    kwargs = kwargs or {}

    it = InterruptableThread()
    it.start()
    it.join(timeout)
    result = getattr(it, 'result', default)
    return result if result is not None else default
