import uuid
from entities.social import SOCIAL_ENUMS
from entities.base import BaseEntity


class Post(BaseEntity):
    PK_PREFIX = "COMPANY#"
    SK_PREFIX = "POST#"

    def __init__(self, item):
        self._item = item
        self.company_id = item["company_id"]
        self.user_id = item["user_id"]
        self.post_title = item["post_title"]
        self.post_content = item["post_content"]
        self.can_share_on = item["can_share_on"]
        self.points_map = item["points_map"]
        self.uuid = str(uuid.uuid4())
        super().__init__()

    def get_keys(self):
        item = self._item
        if item.get("post_id"):
            SK = self.created_at + "#" + Post.SK_PREFIX + item["post_id"]
        else:
            SK = self.created_at + "#" + Post.SK_PREFIX + self.uuid

        PK = Post.PK_PREFIX + self.company_id
        return {"PK": PK, "SK": SK}

    def get_item(self):
        item = dict(self.__dict__)
        item.pop("_item", None)
        item.pop("uuid", None)
        return item

    def get_record(self):
        keys = self.get_keys()
        item = dict(self.__dict__)
        item.pop("_item", None)
        item.pop("uuid", None)
        item.update(keys)
        return item

    @classmethod
    def keys_from_ids_and_date(cls, company_id, post_id, created_at):
        PK = cls.PK_PREFIX + company_id
        SK = created_at + "#" + cls.SK_PREFIX + post_id
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

        if item.get("post_id"):
            self.post_id = item["post_id"]
        else:
            self.post_id = self.uuid

    def _assert(self):
        can_share_on = self.can_share_on
        for element in can_share_on:
            assert element in SOCIAL_ENUMS, "Unsupprted Social Network"
        points_map = self.points_map
        for element in points_map.keys():
            assert element in SOCIAL_ENUMS, "Unsupprted Social Network"

    def __repr__(self):
        post_repr = " ".join(self.post_title.split()[0:3]) + "..."
        return "Post<{} -- {}>".format(post_repr, self.user_id)
