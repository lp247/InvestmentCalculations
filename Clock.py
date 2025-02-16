from typing import Callable


class Clock:
    def __init__(self):
        self.tickListener = []

    def listen(self, function: Callable):
        self.tickListener.append(function)

    def tick(self):
        for listener in self.tickListener:
            listener()


class TimeVariant:
    def __init__(self, clock: Clock):
        self.clock = clock
        clock.listen(self.onTick)

    def onTick(self):
        raise NotImplementedError
