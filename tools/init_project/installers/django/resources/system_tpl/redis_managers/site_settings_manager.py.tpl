import json
from typing import Any
from django_redis import get_redis_connection

REDIS_SITE_SETTINGS_KEY = "site_settings_hash"

class SiteSettingsManager:
    """Manager for handling SiteSettings in Redis."""

    @staticmethod
    def get_redis_client():
        return get_redis_connection("default")

    @classmethod
    def save_to_redis(cls, instance: Any):
        redis_client = cls.get_redis_client()
        settings_dict = instance.to_dict()

        sanitized_dict = {}
        for key, value in settings_dict.items():
            if value is None:
                sanitized_dict[key] = ""
            elif isinstance(value, bool):
                sanitized_dict[key] = "true" if value else "false"
            elif isinstance(value, (dict, list)):
                sanitized_dict[key] = json.dumps(value)
            else:
                sanitized_dict[key] = str(value)

        redis_client.hset(REDIS_SITE_SETTINGS_KEY, mapping=sanitized_dict)

    @classmethod
    def load_from_redis(cls) -> dict:
        redis_client = cls.get_redis_client()
        cached_data = redis_client.hgetall(REDIS_SITE_SETTINGS_KEY)

        if cached_data:
            return {k.decode(): v.decode() for k, v in cached_data.items()}

        from features.system.models.site_settings import SiteSettings
        instance = SiteSettings.load()
        cls.save_to_redis(instance)
        return instance.to_dict()
