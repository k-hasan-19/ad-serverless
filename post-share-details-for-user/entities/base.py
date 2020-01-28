from abc import ABC, abstractmethod

class BaseEntity(ABC):
    
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
    def _date_time_now(self):
        import datetime
        return str(datetime.datetime.utcnow().isoformat('T'))+'Z'