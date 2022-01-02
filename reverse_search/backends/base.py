import abc


class __ReverseSearchBackendMeta(abc.ABCMeta):

    MODEL = None

    def __init__(cls, *args, **kwargs):
        if cls.__name__ != "ReverseSearchBackend" and not cls.MODEL:
            raise ValueError("Backend must define a database model to use.")
        super().__init__(*args, **kwargs)


class ReverseSearchBackend(abc.ABC, metaclass=__ReverseSearchBackendMeta):

    @abc.abstractmethod
    def search(self, query, *args, **kwargs):
        raise NotImplementedError
