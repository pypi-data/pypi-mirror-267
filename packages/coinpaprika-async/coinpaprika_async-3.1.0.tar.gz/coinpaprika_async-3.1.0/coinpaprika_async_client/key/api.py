from typing import Dict, Any

from ..client import CoinPaprikaAsyncClient

from ..networking_layer import ApiError

from .models import KeyInfo, APIUsage, CurrentMonthUsage


class KeyEndpoint:

    def __init__(self) -> None:
        self.__internal = CoinPaprikaAsyncClient()

    async def get_key_info(self) -> ApiError | KeyInfo:
        res = await self.__internal.call_api("key/info")

        if res.Error:
            return res.Error

        data: Dict[str, Any] = res.Data

        return KeyInfo(
            plan=data["plan"],
            plan_started_at=data["plan_started_at"],
            plan_status=data["plan_status"],
            portal_url=data["portal_url"],
            usage=APIUsage(
                message=data["message"],
                current_month=CurrentMonthUsage(
                    requests_left=data["requests_left"],
                    requests_made=data["requests_made"],
                ),
            ),
        )
