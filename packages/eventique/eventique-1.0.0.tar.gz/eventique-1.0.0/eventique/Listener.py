from threading import Timer
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .EventsHandler import EventsHandler


class Listener:
    def __init__(
        self,
        manager: "EventsHandler",
        event_id,
        callback: callable,
        timeout=None,
        ontimeout=None,
        once=False,
        priority=0,
        originator=None,
    ):
        self._deleted = False
        self.event_id = event_id
        self.callback = callback
        self.timeout = timeout
        self.timeoutCallback = ontimeout
        self.timeoutTimer = None
        if timeout:
            self.armTimer()
        self.once = once
        self.priority = priority
        self.manager = manager
        self.originator = originator

    def call(self, event, *args, **kwargs):
        if self._deleted:
            return
        self.cancelTimer()
        self.callback(event, *args, **kwargs)

    def delete(self):
        self._deleted = True
        self.cancelTimer()
        if self.event_id not in self.manager._listeners:
            return
        listeners = self.manager._listeners[self.event_id][self.priority]
        if self in listeners:
            listeners.remove(self)
            if self.event_id in self.manager._sorted:
                del self.manager._sorted[self.event_id]

    def armTimer(self, newTimeout=None):
        if self._deleted:
            return
        if newTimeout:
            self.timeout = newTimeout
        self.timeoutTimer = Timer(self.timeout, lambda: self.timeoutCallback(self))
        self.timeoutTimer.start()

    def cancelTimer(self):
        if self.timeoutTimer:
            self.timeoutTimer.cancel()

    def __str__(self):
        summary = f"Listener(event_id={self.event_id}, priority={self.priority}, callback={self.callback.__name__}, "
        return summary
