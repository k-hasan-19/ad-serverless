from entities.base import BaseEntity
from entities.social import SOCIAL_ENUMS

class ShareEvent(BaseEntity):
    PK_PREFIX = "COMPANY#"
    SK_PREFIX = "POST_SHARE#"
    def __init__(self, item):
        self._item = item
        self.company_id = item["company_id"]
        self.user_id = item["user_id"]
        self.post_id = item["post_id"]
        self.shared_on = item["shared_on"]
        self.points = item["points"]
        self._set_common()
        self._assert()

    def get_keys(self):
        PK = ShareEvent.PK_PREFIX + self.company_id
        SK = ShareEvent.SK_PREFIX + self.post_id+'#'+self.user_id+'#'+self.shared_on
        return {"PK": PK, "SK": SK}

    def get_item(self):
        item = dict(self.__dict__)
        item.pop('_item', None)
        return item

    def get_record(self):
        keys = self.get_keys()
        item = dict(self.__dict__)
        item.pop('_item', None)
        item.update(keys)
        return item

    def _set_common(self):
        item = self._item
        if item.get("created_at"):
            self.created_at = item["created_at"]
        else:
            self.created_at = super()._date_time_now()
            
    def _assert(self):
        shared_on = self.shared_on
        assert shared_on in SOCIAL_ENUMS, 'Unsupprted Social Network'
            
    def __repr__(self):
        return "ShareEvent<{} -- {}>".format(self.user_id, self.shared_on)
        
# {
#   "company_id": "inneed.cloud",
#   "points": 25,
#   "post_id": "353102ba-1cae-4bfb-8a74-a958277b86c9",
#   "shared_on": "LINKEDIN",
#   "user_id": "saif@inneed.cloud"
# }