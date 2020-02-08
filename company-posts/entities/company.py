from entities.base import BaseEntity


class CompanyMeta(BaseEntity):
    PK_PREFIX = "COMPANY#"
    SK_PREFIX = "#METADATA#"

    def __init__(self, item):
        self._item = item
        self.company_id = item["domain"]
        self.domain = item["domain"]
        self.name = item["name"]
        self.address = item["address"]
        super().__init__()

    def get_keys(self):
        PK = CompanyMeta.PK_PREFIX + self.company_id
        SK = CompanyMeta.SK_PREFIX + self.company_id
        return {"PK": PK, "SK": SK}

    def get_item(self):
        item = dict(self.__dict__)
        item.pop("_item", None)
        return item

    def get_record(self):
        keys = self.get_keys()
        item = dict(self.__dict__)
        item.pop("_item", None)
        item.update(keys)
        return item

    @classmethod
    def keys_from_domain(cls, domain):
        PK = cls.PK_PREFIX + domain
        SK = cls.SK_PREFIX + domain
        return (
            PK,
            SK,
        )

    def _set_common(self):
        item = self._item
        if item.get("created_at"):
            self.created_at = item["created_at"]
            self.updated_at = super()._date_time_now()

        else:
            self.created_at = self.updated_at = super()._date_time_now()

    def _assert(self):
        pass

    def __repr__(self):
        return "Company<{} -- {}>".format(self.company_id, self.name)
