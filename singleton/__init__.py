class Singleton(object):
    """Singleton metaclass enforcing a single instance with state preservation."""

    _instances = {}

    def __init__(self, *args, **kwargs):
        if self.__class__ not in self._instances:
            self._instances[self.__class__] = self
            super().__init__(*args, **kwargs)  # Initialize only once
        else:
            # Access attributes from existing instance
            self.__dict__ = self._instances[self.__class__].__dict__

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]
