"""Metrics collection classes."""

import json

from loguru import logger as log
from requests import get


MAP_UNIT = {
    "%": "ratio",
    "°C": "celsius",
    "V": "volts",
    "A": "amperes",
    "W": "watts",
    "Hz": "hertz",
}


def fetch_entity_state(name, config):
    """Fetch the given entity's state from HomeAssistant.

    Parameters
    ----------
    name : str
        The HomeAssistant entity name (without prefix).
    config : Box
        The service configuration object, see config.load_config_file() for
        more details.

    Returns
    -------
    dict
        The dict parsed from the JSON response delivered by HomeAssistant.
    """
    url = f"{config.homeassistant.api_url}/states/{config.entity_pfx}_{name}"
    headers = {
        "Authorization": f"Bearer {config.homeassistant.token}",
        "content-type": "application/json",
    }
    log.trace(f"Requesting [{url}]...")
    response = get(url, headers=headers, timeout=10)
    state = json.loads(response.text)
    return state


def new_metric(state, metric_type, config):
    """Create a new Prometheus metric of the given type.

    Parameters
    ----------
    state : dict
        The corresponding entity state for which the metric should be created,
        as delivered by fetch_entity_state(). Used to derive the metric's name
        and attributes.
    metric_type : prometheus_client.Counter or prometheus_client.Gauge
        The metric type to be created.
    config : Box
        The service configuration object, see config.load_config_file() for
        more details.

    Returns
    -------
    prometheus_client.Counter or prometheus_client.Gauge
        The new Prometheus metric object.
    """
    cut = len(config.entity_pfx) + 1
    name = state["entity_id"][cut:]
    attributes = state["attributes"]
    try:
        unit = MAP_UNIT.get(attributes["unit_of_measurement"])
    except KeyError:
        unit = ""
    docs = attributes["friendly_name"]
    prefix = config.metric_pfx
    return metric_type(name=f"{prefix}_{name}", documentation=docs, unit=unit)
