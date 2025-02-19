from typing import Callable, List


class Clock:
    def __init__(self):
        self.tickListener: List[Callable[[], None]] = []

    def listen(self, function: Callable[[], None]):
        self.tickListener.append(function)

    def tick(self):
        for listener in self.tickListener:
            listener()
