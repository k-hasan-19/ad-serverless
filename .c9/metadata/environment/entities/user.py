{"filter":false,"title":"user.py","tooltip":"/entities/user.py","undoManager":{"mark":0,"position":0,"stack":[[{"start":{"row":0,"column":0},"end":{"row":60,"column":0},"action":"remove","lines":["from entities.base import BaseEntity","","","class UserMeta(BaseEntity):","    PK_PREFIX = \"COMPANY#\"","    SK_PREFIX = \"USER#\"","","    def __init__(self, item):","        self._item = item","        self.company_id = item[\"domain\"]","        self.user_id = item[\"email\"]","        self.domain = item[\"domain\"]","        self.email = item[\"email\"]","        self.first_name = item[\"first_name\"]","        self.last_name = item[\"last_name\"]","        super().__init__()","","    def get_keys(self):","        PK = UserMeta.PK_PREFIX + self.company_id","        SK = UserMeta.SK_PREFIX + self.user_id","        return {\"PK\": PK, \"SK\": SK}","","    def get_item(self):","        item = dict(self.__dict__)","        item.pop(\"_item\", None)","        return item","","    def get_record(self):","        keys = self.get_keys()","        item = dict(self.__dict__)","        item.pop(\"_item\", None)","        item.update(keys)","        return item","","    @classmethod","    def keys_from_ids(cls, company_id, user_id):","        PK = cls.PK_PREFIX + company_id","        SK = cls.SK_PREFIX + user_id","        return (","            PK,","            SK,","        )","","    def _set_common(self):","        item = self._item","        if item.get(\"created_at\"):","            self.created_at = item[\"created_at\"]","            self.updated_at = item[\"updated_at\"]","        else:","            self.created_at = self.updated_at = super()._date_time_now()","        if not item.get(\"is_admin\"):","            self.is_admin = False","        else:","            self.is_admin = bool(item[\"is_admin\"])","","    def _assert(self):","        pass","","    def __repr__(self):","        return \"User<{} -- {}>\".format(self.user_id, self.company_id)",""],"id":19},{"start":{"row":0,"column":0},"end":{"row":60,"column":0},"action":"insert","lines":["from entities.base import BaseEntity","","","class UserMeta(BaseEntity):","    PK_PREFIX = \"COMPANY#\"","    SK_PREFIX = \"USER#\"","","    def __init__(self, item):","        self._item = item","        self.company_id = item[\"company_id\"]","        self.user_id = item[\"user_id\"]","        self.email = item[\"email\"]","        self.first_name = item[\"first_name\"]","        self.last_name = item[\"last_name\"]","        super().__init__()","","    def get_keys(self):","        PK = UserMeta.PK_PREFIX + self.company_id","        SK = UserMeta.SK_PREFIX + self.user_id","        return {\"PK\": PK, \"SK\": SK}","","    def get_item(self):","        item = dict(self.__dict__)","        item.pop(\"_item\")","        return item","","    def get_record(self):","        keys = self.get_keys()","        item = dict(self.__dict__)","        _item = item.pop(\"_item\")","        item.update(keys)","        item.update(_item)","        return item","","    @classmethod","    def keys_from_ids(cls, company_id, user_id):","        PK = cls.PK_PREFIX + company_id","        SK = cls.SK_PREFIX + user_id","        return (","            PK,","            SK,","        )","","    def _set_common(self):","        item = self._item","        if item.get(\"created_at\"):","            self.created_at = item[\"created_at\"]","            self.updated_at = item[\"updated_at\"]","        else:","            self.created_at = self.updated_at = super()._date_time_now()","        if not item.get(\"is_admin\"):","            self.is_admin = False","        else:","            self.is_admin = bool(item[\"is_admin\"])","","    def _assert(self):","        pass","","    def __repr__(self):","        return \"User<{} -- {}>\".format(self.user_id, self.company_id)",""]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":31,"column":26},"end":{"row":31,"column":26},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1581057491299,"hash":"b0015d070bee371f557b5f52913af8cdcbb324d3"}