class observer():
    _observers = []
    def __init__(self):
        self._observers.append(self)
        self._observables = {}
    def observe(self, event_name, callback):
        self._observables[event_name] = callback


class Event():
    def __init__(self, callbackname, generator=None, param=None, autofire = True):
        self.generator = generator
        self.param = param
        self.callbackname = callbackname

        if autofire:
            self.fire()
    def fire(self):
        for obs in observer._observers:
            if self.callbackname in obs._observables:
                if self.param:
                    obs._observables[self.callbackname](self.generator, self.param)
                elif self.generator:
                    obs._observables[self.callbackname](self.generator)
                else :
                    obs._observables[self.callbackname]()