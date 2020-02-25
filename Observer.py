class Observer():
    _observers = []
    def __init__(self):
        self._observers.append(self)
        self._observables = {}
    def observe(self, event_name, callback):
        self._observables[event_name] = callback


class Event():
    def __init__(self, callbackname, generator=None, autofire = True):
        self.generator = generator
        self.callbackname = callbackname

        if autofire:
            self.fire()
    def fire(self):
        for observer in Observer._observers:
            if self.callbackname in observer._observables:
                if self.generator:
                    observer._observables[self.callbackname](self.generator)
                else :
                    observer._observables[self.callbackname]()