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

import asyncio as asyncio_module
import atexit
import logging
import os
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Union

from . import constants, logging_messages, optional_update
from .connection import MPM_BASE_PATH, REST_API_BASE_PATH
from .connection_helpers import sanitize_url, url_join
from .environment import check_environment
from .events import events_from_dataframe
from .events.label_event import LabelEvent
from .events.prediction_event import PredictionEvent
from .logging_messages import MPM_JOIN_DEPRECATED_WARNING
from .sender import get_sender
from .settings import MPMSettings, get_model
from .settings_helper import extract_comet_url

LOGGER = logging.getLogger(__name__)

LogEventsResult = Union[List[Any], Awaitable[List[Any]]]


class CometMPM:
    """
    The Comet MPM class is used to upload a model's input and output features to MPM
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_name: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        disabled: Optional[bool] = None,
        asyncio: bool = False,
        max_batch_size: Optional[int] = None,
        max_batch_time: Optional[int] = None,
    ):
        """
        Creates the Comet MPM Event logger object.
        Args:
            api_key: The Comet API Key
            workspace_name: The Comet Workspace Name of the model
            model_name: The Comet Model Name of the model
            model_version: The Comet Model Version of the model
            disabled: If set to True, CometMPM will not send anything to the backend.
            asyncio: Set to True if you are using an Asyncio-based framework like FastAPI.
            max_batch_size: Maximum number of MPM events sent in a batch, can also be configured using the environment variable MPM_MAX_BATCH_SIZE.
            max_batch_time: Maximum time before a batch of events is submitted to MPM, can also be configured using the environment variable MPM_MAX_BATCH_SIZE.
        """

        settings_user_values = {}  # type: Dict[str, str|int]
        optional_update.update(
            settings_user_values,
            {
                "api_key": api_key,
                "mpm_model_name": model_name,
                "mpm_model_version": model_version,
                "mpm_workspace_name": workspace_name,
                "mpm_max_batch_size": max_batch_size,
                "mpm_max_batch_time": max_batch_time,
            },
        )

        self._settings = get_model(
            MPMSettings,
            **settings_user_values,
        )
        if disabled:
            self.disabled = disabled  # type: bool
        else:
            self.disabled = bool(os.getenv("COMET_MPM_DISABLED"))
        self._asyncio = asyncio

        comet_url = sanitize_url(extract_comet_url(self._settings))

        self._mpm_url = url_join(comet_url, MPM_BASE_PATH)
        self._api_url = url_join(comet_url, REST_API_BASE_PATH)

        if self.disabled:
            self._sender = None
        else:
            self._sender = get_sender(
                api_key=self._settings.api_key,
                server_address=self._mpm_url,
                max_batch_size=self._settings.mpm_max_batch_size,
                max_batch_time=self._settings.mpm_max_batch_time,
                asyncio=self._asyncio,
                batch_sending_timeout=self._settings.mpm_batch_sending_timeout,
            )

            atexit.register(self._on_end)

        check_environment()

    def log_event(
        self,
        prediction_id: str,
        input_features: Optional[Dict[str, Any]] = None,
        output_value: Optional[Any] = None,
        output_probability: Optional[Any] = None,
        output_features: Optional[Dict[str, Any]] = None,
        timestamp: Optional[float] = None,
    ) -> Optional[Awaitable[None]]:
        """
        Asynchronously log a single event to MPM. Events are identified by the
        mandatory prediction_id parameter. You can send multiple events with
        the same prediction_id, and the events will be automatically merged
        on the backend side.

        Args:
            prediction_id: The unique prediction ID. It can be provided by the
                framework, you, or a random unique value such as str(uuid4()).
            input_features: If provided, it must be a flat dictionary where the
                keys are the feature names, and the values are native Python
                scalars, such as integers, floats, booleans, or strings. For
                example: `{"age": 42, "income": 42894.89}`.
            output_value: The prediction as a native Python scalar, such as an
                 integer, float, boolean, or string.
            output_probability: If provided, it must be a float between 0 and
                 1, indicating the model's confidence in the prediction.
            output_features: A dictionary of output features.
            timestamp: An optional timestamp to associate with the event
                (seconds since epoch in UTC timezone). If not provided, the
                 current time will be used."""
        if self.disabled:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

        output_features = _handle_event_output_features(
            output_value, output_probability, output_features
        )

        event = PredictionEvent(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            prediction_id=prediction_id,
            input_features=input_features,
            output_features=output_features,
            timestamp=timestamp,
        )
        return self._log_event(event)

    def log_label(self, prediction_id: str, label: Any) -> Optional[Awaitable[None]]:
        """
        Send an MPM event containing the ground truth value for a prediction whose input and output
        features are already stored in Comet.
        Args:
            prediction_id: The unique prediction ID
            label: The ground truth value for the prediction
        """
        if self.disabled:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

        event = LabelEvent(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            prediction_id=prediction_id,
            label=label,
        )
        return self._log_event(event)

    def log_dataframe(  # type: ignore[no-untyped-def]
        self,
        dataframe,
        prediction_id_column: str,
        feature_columns: Optional[List[str]] = None,
        output_value_column: Optional[str] = None,
        output_probability_column: Optional[str] = None,
        output_features_columns: Optional[List[str]] = None,
        timestamp_column: Optional[str] = None,
    ) -> LogEventsResult:
        """
        This function logs each row of a Pandas DataFrame as an MPM event. The
        events are structured as described in the [log_event](#cometmpmlog_event)
        method, so please refer to it for full context.

        Args:
            dataframe: The Pandas DataFrame to be logged.
            prediction_id_column: This column should contain the prediction_id values for the
                events.
            feature_columns: If provided, these columns will be used as the input_features
                for the events.
            output_features_columns: If provided, these columns will be used as the output_features for the events.
            output_value_column: Deprecated, please use the output_features_column field instead. If provided, this
                column will be used as the output_value for the events.
            output_probability_column: Deprecated, please use the output_features_column field instead.
                If provided, this column will be used as the output_probability for the events.
            timestamp_column: If provided, this column will be used as the timestamp (seconds since
                epoch start in UTC timezone) for the events.
        """
        events = events_from_dataframe.generate(
            workspace=self._settings.mpm_workspace_name,
            model_name=self._settings.mpm_model_name,
            model_version=self._settings.mpm_model_version,
            dataframe=dataframe,
            prediction_id_column=prediction_id_column,
            feature_columns=feature_columns,
            output_features_columns=output_features_columns,
            output_value_column=output_value_column,
            output_probability_column=output_probability_column,
            timestamp_column=timestamp_column,
        )

        return self._log_events(events)

    def connect(self) -> None:
        """
        When using CometMPM in asyncio mode, this coroutine needs to be awaited
        at the server start.
        """
        if self._sender is not None:
            self._sender.connect()

    def join(self, timeout: Optional[int] = None) -> Optional[Awaitable[None]]:
        """
        MPM.join is deprecated, use MPM.end instead.
        """
        LOGGER.warning(MPM_JOIN_DEPRECATED_WARNING)
        return self.end(timeout)

    def end(self, timeout: Optional[int] = None) -> Optional[Awaitable[None]]:
        """Ensure that all data has been sent to Comet and close the MPM object.
        After that, no data can be logged anymore. Waits for up to 30 seconds if timeout is not set.
        """
        if timeout is None:
            timeout = self._settings.mpm_join_timeout

        if not self.disabled:
            assert self._sender is not None
            if self._asyncio:
                return self._sender.join(timeout)
            else:
                self._sender.close(timeout)

        if self._asyncio is False:
            return None
        else:
            return asyncio_module.sleep(0)

    def _on_end(self) -> None:
        if not self.disabled:
            assert self._sender is not None
            self._sender.close(timeout=self._settings.mpm_join_timeout)

    def _log_events(self, events: Iterable[PredictionEvent]) -> LogEventsResult:
        results = []
        for event in events:
            result = self._log_event(event)
            if result is not None:
                results.append(result)

        if self._asyncio and len(results) > 0:
            return asyncio_module.gather(*results)

        return results

    def _log_event(
        self, event: Union[PredictionEvent, LabelEvent]
    ) -> Optional[Awaitable[None]]:
        assert self._sender is not None
        return self._sender.put(event)


def _handle_event_output_features(
    output_value: Any,
    output_probability: Any,
    output_features: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    event_output_features: Optional[Dict[str, Any]]

    if (
        output_value is not None or output_probability is not None
    ) and output_features is None:
        LOGGER.warning(
            logging_messages.DEPRECATED_OUTPUT_VALUE_AND_PROBABILITY_WITHOUT_FEATURES
        )

        event_output_features = {}
        if output_value is not None:
            event_output_features[constants.EVENT_PREDICTION_VALUE] = output_value

        if output_probability is not None:
            event_output_features[
                constants.EVENT_PREDICTION_PROBABILITY
            ] = output_probability
    elif (
        output_value is not None and output_probability is not None
    ) and output_features is not None:
        LOGGER.warning(
            logging_messages.DEPRECATED_OUTPUT_VALUE_AND_PROBABILITY_WITH_FEATURES
        )

        event_output_features = {
            constants.EVENT_PREDICTION_VALUE: output_value,
            constants.EVENT_PREDICTION_PROBABILITY: output_probability,
        }
        for key in output_features:
            event_output_features[key] = output_features[key]
    else:
        event_output_features = output_features

    return event_output_features
