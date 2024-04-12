import operator
import threading
from typing import Any
from .Listener import Listener

lock = threading.RLock()


class Event(object):
    propagation_stopped = False
    sender: "EventsHandler"
    name: Any
    listener: "Listener"

    def stop_propagation(self):
        self.propagation_stopped = True


class EventsHandler:
    def __init__(self):
        super().__init__()
        self._listeners = dict[str, dict[int, list[Listener]]]()
        self._sorted = {}
        self.__waiting_events = list[threading.Event]()
        self._crashMessage = None

    def hasListener(self, event_id):
        """
        Check if an event has listeners
        Args:
            event_id (str): event to check
        Returns:
            bool: True if the event has listeners, False otherwise
        """
        return event_id in self._listeners

    def wait(self, event, timeout: float = None, originator=None):
        """
        Wait for an event to be triggered, return the args and kwargs of the event
        Args:
            event (str): event to wait for
            timeout (float, optional): timeout in seconds. Defaults to None.
            originator ([type], optional): [description]. Defaults to None.
            Raises:
                TimeoutError: if the event is not triggered before the timeout
                Returns:
                    tuple: args, kwargs of the event
        """
        received = threading.Event()
        ret = [None]

        def onReceived(e, *args, **kwargs):
            received.set()
            ret[0] = *args, *kwargs

        self.once(event, onReceived, originator=originator)
        self.__waiting_events.append(received)
        wait_result = received.wait(timeout)
        if received in self.__waiting_events:
            self.__waiting_events.remove(received)
        if self._crashMessage:
            raise Exception(self._crashMessage)
        if not wait_result:
            raise TimeoutError(f"wait event {event} timed out")
        return ret[0]

    def on(
        self,
        event_id,
        callback,
        priority=0,
        timeout=None,
        ontimeout=None,
        once=False,
        originator=None,
        retryNbr=None,
        retryAction=None,
    ):
        """
        Register a callback for an event
        Args:
            event_id (str): event to listen to
            callback (callable): callback to call when the event is triggered
            priority (int, optional): priority of the listener. Defaults to 0.
            timeout (float, optional): timeout in seconds. Defaults to None.
            ontimeout (callable, optional): callback to call when the timeout is reached. Defaults to None.
            once (bool, optional): True if the listener should be removed after the first trigger. Defaults to False.
            originator ([type], optional): [description]. Defaults to None.
            retryNbr ([type], optional): [description]. Defaults to None.
            retryAction ([type], optional): [description]. Defaults to None.
            Raises:
                ValueError: if the callback is not callable
            Returns: Listener: the listener object
        """
        if not callable(callback):
            raise ValueError("callback must be callable")
        if event_id not in self._listeners:
            self._listeners[event_id] = {}
        if priority not in self._listeners[event_id]:
            self._listeners[event_id][priority] = []

        def onListenerTimeout(listener: Listener):
            if retryNbr:
                listener.nbrTimeouts += 1
                if listener.nbrTimeouts > retryNbr:
                    return ontimeout(listener)
                listener.armTimer()
                if retryAction:
                    retryAction()
            else:
                ontimeout(listener)

        listener = Listener(self, event_id, callback, timeout, onListenerTimeout, once, priority, originator)
        if event_id not in self._listeners:
            return
        self._listeners[event_id][priority].append(listener)
        if event_id in self._sorted:
            del self._sorted[event_id]
        return listener

    def onMultiple(self, listeners, originator=None):
        """
        Register multiple listeners at once
        Args:
            listeners (list[tuple]): list of tuples (event_id, callback) or (event_id, callback, kwargs)
            originator ([type], optional): [description]. Defaults to None.
        Raises:
            ValueError: if the listener_args are not valid
        """
        for listener_args in listeners:
            if len(listener_args) == 2:
                event_id, callback = listener_args
                self.on(event_id, callback, originator=originator)
            elif len(listener_args) == 3:
                event_id, callback, kwargs = listener_args
                self.on(event_id, callback, **kwargs, originator=originator)
            else:
                raise ValueError("Invalid listener_args, must be a tuple of 2 or 3 elements (event_id, callback) or (event_id, callback, kwargs)")

    def once(
        self,
        event_id,
        callback,
        priority=0,
        timeout=None,
        ontimeout=None,
        originator=None,
        retryNbr=None,
        retryAction=None,
    ):
        """
        Register a callback for an event that will be removed after the first trigger
        Args:
            event_id (str): event to listen to
            callback (callable): callback to call when the event is triggered
            priority (int, optional): priority of the listener. Defaults to 0.
            timeout (float, optional): timeout in seconds. Defaults to None.
            ontimeout (callable, optional): callback to call when the timeout is reached. Defaults to None.
            originator ([type], optional): [description]. Defaults to None.
            retryNbr ([type], optional): [description]. Defaults to None.
            retryAction ([type], optional): [description]. Defaults to None.
        Raises:
            ValueError: if the callback is not callable
        """
        return self.on(
            event_id,
            callback,
            priority,
            timeout,
            ontimeout,
            once=True,
            originator=originator,
            retryNbr=retryNbr,
            retryAction=retryAction,
        )

    def sort_listeners(self, event_id):
        """
        Sort the listeners by priority
        Args:
            event_id (str): event to sort
        """
        self._sorted[event_id] = []
        if event_id in self._listeners:
            self._sorted[event_id] = [
                listener
                for listeners in sorted(self._listeners[event_id].items(), key=operator.itemgetter(0))
                for listener in listeners[1]
            ]

    def getSortedListeners(self, event_id=None) -> list[Listener]:
        """
        Get the listeners sorted by priority
        Args:
            event_id (str, optional): event to get the listeners from. Defaults to None.
        Returns:
            list[Listener]: list of listeners sorted by priority
        """
        if event_id is not None:
            if event_id not in self._sorted:
                self.sort_listeners(event_id)
            return self._sorted[event_id]

        for event_id in self._listeners:
            if not event_id in self._sorted:
                self.sort_listeners(event_id)

    def send(self, event_id, *args, **kwargs):
        """
        Trigger an event
        Args:
            event_id (str): event to trigger
            *args: args to pass to the listeners
            **kwargs: kwargs to pass to the listeners
        Returns:
            Event: the event object
        """
        event = Event()
        event.sender = self
        event.name = event_id
        listeners = self._listeners.get(event_id, [])
        if not listeners:
            return event
        event_listeners = self.getSortedListeners(event_id)
        to_remove = list[Listener]()
        for listener in event_listeners:
            event = Event()
            event.sender = self
            event.name = event_id
            event.listener = listener
            listener.call(event, *args, **kwargs)
            if listener.once:
                to_remove.append(listener)
            if event.propagation_stopped:
                break
        with lock:
            if to_remove:
                if event_id in self._sorted:
                    del self._sorted[event_id]
                for listener in to_remove:
                    listener.delete()

    def reset(self):
        """
        Reset the event handler
        """
        self.stopAllEventsWaits()
        for listener in self.iterListeners():
            listener.delete()
        self._listeners.clear()
        self._sorted.clear()

    def iterListeners(self):
        """
        Iterate over all the listeners
        Yields:
            Listener: the next listener
        """
        for listenersByPrio in self._listeners.values():
            for listeners in listenersByPrio.values():
                for listener in listeners:
                    yield listener

    def stopAllEventsWaits(self):
        """
        Stop all the events waits
        """
        for evt in self.__waiting_events:
            evt.set()
        self.__waiting_events.clear()

    def remove_listeners(self, event_id, callbacks) -> list:
        """
        Remove listeners from an event
        Args:
            event_id (str): event to remove the listeners from
            callbacks (list): list of callbacks to remove
        Returns:
            list: list of listeners removed
        """
        if event_id not in self._listeners:
            return
        for _, listeners in self._listeners[event_id].items():
            listeners = list(filter(lambda l: l.callback not in callbacks, listeners))
        if event_id in self._sorted:
            del self._sorted[event_id]

    def remove_listener(self, event_id, callback):
        """
        Remove a listener from an event
        Args:
            event_id (str): event to remove the listener from
            callback (callable): callback to remove
        """
        if event_id not in self._listeners:
            return
        for _, listeners in self._listeners[event_id].items():
            listeners = list(filter(lambda l: l.callback != callback, listeners))
        if event_id in self._sorted:
            del self._sorted[event_id]

    def getListenersByOrigin(self, origin) -> list[Listener]:
        """
        Get all the listeners from an origin
        Args:
            origin ([type]): [description]
        Returns:
            list: list of listeners
        """
        result = list[Listener]()
        for listenersByPrio in self._listeners.values():
            for listeners in listenersByPrio.values():
                for listener in listeners:
                    if listener.originator and listener.originator == origin:
                        result.append(listener)
        return result

    def clearAllByOrigin(self, origin):
        """
        Clear all the listeners from an origin
        Args:
            origin ([type]): [description]
        """
        toBeDeleted = self.getListenersByOrigin(origin)
        for listener in toBeDeleted:
            listener.delete()
