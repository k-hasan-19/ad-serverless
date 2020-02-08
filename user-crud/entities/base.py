from abc import ABC, abstractmethod


class BaseEntity(ABC):
    def __init__(self):
        self._set_common()
        self._assert()

    @property
    @abstractmethod
    def PK_PREFIX(self):
        pass

    @property
    @abstractmethod
    def SK_PREFIX(self):
        pass

    @abstractmethod
    def get_keys(self):
        pass

    @abstractmethod
    def get_item(self):
        pass

    @abstractmethod
    def get_record(self):
        pass

    @abstractmethod
    def _set_common(self):
        pass

    @abstractmethod
    def _assert(self):
        pass

    def _date_time_now(self):
        import datetime

        return (
            str(datetime.datetime.utcnow().replace(microsecond=0).isoformat("T")) + "Z"
        )
