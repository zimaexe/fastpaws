import json
from typing import Type, Optional
import redis.asyncio as redis


class RedisClient:
    _instance: Optional["RedisClient"] = None

    def __new__(cls) -> "RedisClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.redis = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True
            )
        return cls._instance

    async def get_conversation_data(self, chat_id):
        result = (await self._instance.redis.get(f"chat:{chat_id}"))
        return json.loads(result) if result else []

    async def set_conversation_data(self, chat_id, data):
        history = await self.get_conversation_data(chat_id)
        await self._instance.redis.set(f"chat:{chat_id}", json.dumps(history + data))

    async def get_patient_id(self, chat_id):
        return await self._instance.redis.get(f"patient_id:{chat_id}")

    async def set_patient_id(self, chat_id, patient_id):
        await self._instance.redis.set(f"patient_id:{chat_id}", patient_id)


REDIS_CLIENT = RedisClient()
