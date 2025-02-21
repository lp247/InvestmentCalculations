from typing import Callable, List


class Clock:
    def __init__(self):
        self.tickListener: List[Callable[[], None]] = []
        self.epoch = 0

    def listen(self, function: Callable[[], None]):
        self.tickListener.append(function)

    def tick(self):
        self.epoch += 1
        for listener in self.tickListener:
            listener()
