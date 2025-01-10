"""
This module provides an interface to interact with a Redis database for storing and retrieving conversation data and patient IDs.

Classes:
    RedisClient:
        A singleton class to manage Redis connections and perform operations such as getting and setting conversation data and patient IDs.

Functions:
    get_conversation_data(chat_id: str) -> list:
        Retrieve the conversation data for a given chat ID from Redis.

    set_conversation_data(chat_id: str, data: list) -> None:
        Store the conversation data for a given chat ID in Redis.

    get_patient_id(chat_id: str) -> Optional[str]:
        Retrieve the patient ID for a given chat ID from Redis.

    set_patient_id(chat_id: str, patient_id: str) -> None:
        Store the patient ID for a given chat ID in Redis.

Dependencies:
    - json
    - redis.asyncio
"""
import json
from typing import Optional

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

    async def get_conversation_data(self, chat_id) -> list:
        """
        Retrieve the conversation data for a given chat ID from Redis.

        Args:
            chat_id (str): The chat ID.

        Returns:
            list: The conversation data.
        """
        result = (await self._instance.redis.get(f"chat:{chat_id}"))
        return json.loads(result) if result else []

    async def set_conversation_data(self, chat_id, data) -> None:
        """
        Store the conversation data for a given chat ID in Redis.

        Args:
            chat_id (str): The chat ID.
            data (list): The conversation data to store.
        """
        history = await self.get_conversation_data(chat_id)
        await self._instance.redis.set(f"chat:{chat_id}", json.dumps(history + data))

    async def get_patient_id(self, chat_id) -> Optional[str]:
        """
        Retrieve the patient ID for a given chat ID from Redis.

        Args:
            chat_id (str): The chat ID.
        """
        return await self._instance.redis.get(f"patient_id:{chat_id}")

    async def set_patient_id(self, chat_id, patient_id) -> None:
        """
        Store the patient ID for a given chat ID in Redis.

        Args:
            chat_id (str): The chat ID.
            patient_id (str): The patient ID.
        """
        await self._instance.redis.set(f"patient_id:{chat_id}", patient_id)


REDIS_CLIENT = RedisClient()
