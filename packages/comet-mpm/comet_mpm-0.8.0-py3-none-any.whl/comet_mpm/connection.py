# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import logging
from typing import Any, Optional

import aiohttp
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .logging_messages import BATCH_SENDING_ERROR

LOGGER = logging.getLogger(__name__)

MPM_BASE_PATH = "/mpm/"
REST_API_BASE_PATH = "/api/v2/"


def get_retry_strategy() -> Retry:
    # The total backoff sleeping time is computed like that:
    # backoff = 2
    # total = 3
    # s = lambda b, i: b * (2 ** (i - 1))
    # sleep = sum(s(backoff, i) for i in range(1, total + 1))

    return Retry(
        total=3,
        backoff_factor=2,
        allowed_methods=None,
    )  # Will wait up to 24s


def get_http_session(retry_strategy: Optional[Retry] = None) -> Session:
    session = Session()

    # Setup retry strategy if asked
    if retry_strategy is not None:
        session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    return session


def send_batch_requests(
    session: Session,
    url_endpoint: str,
    api_key: str,
    batch_sending_timeout: int,
    batch: Any,
) -> None:
    try:
        headers = {"Authorization": api_key}
        response = session.post(
            url_endpoint, headers=headers, json=batch, timeout=batch_sending_timeout
        )
        response.raise_for_status()
        # TODO: Process response
    except Exception:
        LOGGER.error(BATCH_SENDING_ERROR, exc_info=True)


async def send_asyncio_batch_requests(
    session: aiohttp.ClientSession,
    url_endpoint: str,
    api_key: str,
    batch_sending_timeout: int,
    batch: Any,
) -> None:
    try:
        headers = {"Authorization": api_key}
        response = await session.post(
            url_endpoint, headers=headers, json=batch, timeout=batch_sending_timeout
        )
        response.raise_for_status()
    except Exception:
        LOGGER.error(BATCH_SENDING_ERROR, exc_info=True)
