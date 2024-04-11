"""Kucoin Futures WebSocket module."""

import asyncio
import logging
from typing import Union, Callable, Awaitable, Optional

from kucoin_futures.client import WsToken
from kucoin_futures.ws_client import KucoinFuturesWsClient

from kucoin_futures_lib.handlers import OcoHandler, EntryRangeHandler, HandlerABC

logger = logging.getLogger(__name__)


class KucoinFuturesWebsocket:
    """Kucoin Futures user wrapper class."""

    def __init__(self, token: WsToken):
        self.token = token

    async def subscribe(
        self, handler: HandlerABC, timeout: Optional[float] = 60 * 60 * 12
    ) -> None:
        """Subscribe to the WebSocket topic.
        :param handler: Handler object
        :param timeout: Timeout in seconds. Default is 12 hours
        :raises asyncio.TimeoutError: If the timeout is reached
        """
        ws_client = await KucoinFuturesWsClient.create(
            loop=None,
            client=self.token,
            callback=handler.handle,
            private=handler.private,
        )
        await ws_client.subscribe(handler.topic)
        logger.info("%s subscribed to %s", handler, handler.topic)
        try:
            if timeout:
                await asyncio.wait_for(handler.done.wait(), timeout)
            else:
                await handler.done.wait()
        except asyncio.TimeoutError:
            handler.done.set()
            raise asyncio.TimeoutError(f"Timeout reached for {handler}")
        finally:
            logger.info("Unsubscribing from %s", handler.topic)
            # noinspection PyAsyncCall
            asyncio.create_task(ws_client.unsubscribe(handler.topic))

    async def listen_for_entry(
        self,
        instrument: str,
        entry_high: float,
        entry_low: float,
        timeout: float = 60 * 60 * 12,
    ) -> None:
        """Listen for the entry price range.
        :param instrument: Instrument symbol
        :param entry_high: Entry high price
        :param entry_low: Entry low price
        :param timeout: timeout in seconds. Default is 12 hours
        :raises asyncio.TimeoutError: If the timeout is reached
        """
        handler = EntryRangeHandler(
            instrument=instrument, entry_high=entry_high, entry_low=entry_low
        )
        await self.subscribe(handler, timeout)

    async def tp_sl_cancel(
        self,
        instrument: str,
        tp_order_id: str,
        sl_order_id: str,
        cancel_order: Union[Callable[[str], None], Callable[[str], Awaitable[None]]],
    ) -> None:
        """Listen for take profit and stop loss orders and cancel the other order when one is done.
        :param instrument: Instrument symbol
        :param tp_order_id: Take profit order ID, must be a limit order.
        :param sl_order_id: Stop loss order ID, must be a market stop order.
        :param cancel_order: Function to cancel the order
        """
        handler = OcoHandler(
            limit_order_id=tp_order_id,
            market_order_id=sl_order_id,
            instrument=instrument,
            cancel_order=cancel_order,
        )
        await self.subscribe(handler, None)
