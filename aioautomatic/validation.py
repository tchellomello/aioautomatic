"""API Response validation."""
from datetime import datetime

import voluptuous as vol


def timestamp(value):
    """Check that input is a datetime and return the timestamp."""
    if not isinstance(value, datetime):
        raise vol.Invalid("Timestamp must be a datetime object.")

    return value.timestamp()


def opt(key):
    """Create an optional key that returns a default of None."""
    return vol.Optional(key, default=None)


def coerce_datetime(value):
    """Coerce a value to datetime."""
    try:
        return datetime.strptime(value, vol.Datetime.DEFAULT_FORMAT)
    except (TypeError, ValueError):
        raise vol.DatetimeInvalid(
            'Value does not match expected format {}'.format(
                vol.Datetime.DEFAULT_FORMAT))


OPT_STR = vol.Any(str, None)
OPT_INT = vol.Any(int, None)
OPT_FLOAT = vol.Any(float, None)
OPT_DATETIME = vol.Any(coerce_datetime, None)


_REQUEST_BASE = vol.Schema({}, required=False)

VEHICLES_REQUEST = _REQUEST_BASE.extend({
    "created_at__lte": timestamp,
    "created_at__gte": timestamp,
    "updated_at__lte": timestamp,
    "updated_at__gte": timestamp,
    "vin": str,
    "page": vol.All(int, vol.Range(min=1)),
    "limit": vol.All(int, vol.Range(min=1, max=250)),
})

TRIPS_REQUEST = _REQUEST_BASE.extend({
    "started_at__lte": timestamp,
    "started_at__gte": timestamp,
    "ended_at__lte": timestamp,
    "ended_at__gte": timestamp,
    "vehicle": str,
    "tags__in": str,
    "page": vol.All(int, vol.Range(min=1)),
    "limit": vol.All(int, vol.Range(min=1, max=250)),
})

_RESPONSE_BASE = vol.Schema({}, required=True, extra=vol.REMOVE_EXTRA)

AUTH_TOKEN = _RESPONSE_BASE.extend({
    "access_token": str,
    "expires_in": int,
    "scope": str,
    "refresh_token": str,
    "token_type": vol.In(["Bearer"]),
})

LIST_METADATA = _RESPONSE_BASE.extend({
    "count": vol.All(int, vol.Range(min=0)),
    "next": OPT_STR,
    "previous": OPT_STR,
})

LIST_RESPONSE = _RESPONSE_BASE.extend({
    "_metadata": LIST_METADATA,
    "results": [],
})

VEHICLE = _RESPONSE_BASE.extend({
    "url": str,
    "id": str,
    opt("vin"): OPT_STR,
    opt("created_at"): coerce_datetime,
    opt("updated_at"): coerce_datetime,
    opt("make"): OPT_STR,
    opt("model"): OPT_STR,
    opt("year"): OPT_INT,
    opt("submodel"): OPT_STR,
    opt("display_name"): OPT_STR,
    opt("fuel_grade"): OPT_STR,
    opt("fuel_level_percent"): vol.Any(float, None),
    opt("battery_voltage"): vol.Any(float, None),
})

LOCATION = _RESPONSE_BASE.extend({
    "lat": float,
    "lon": float,
    "accuracy_m": float,
})

ADDRESS = _RESPONSE_BASE.extend({
    opt("name"): OPT_STR,
    opt("display_name"): OPT_STR,
    opt("street_number"): OPT_STR,
    opt("streen_name"): OPT_STR,
    opt("city"): OPT_STR,
    opt("state"): OPT_STR,
    opt("country"): OPT_STR,
})

VEHICLE_EVENT = _RESPONSE_BASE.extend({
    "type": str,
    opt("lat"): OPT_FLOAT,
    opt("lon"): OPT_FLOAT,
    opt("created_at"): coerce_datetime,
    opt("g_force"): OPT_FLOAT,
})

TRIP = _RESPONSE_BASE.extend({
    "url": str,
    "id": str,
    "driver": OPT_STR,
    opt("user"): OPT_STR,
    opt("started_at"): OPT_DATETIME,
    opt("ended_at"): OPT_DATETIME,
    opt("distance_m"): OPT_FLOAT,
    opt("duration_s"): OPT_FLOAT,
    opt("vehicle"): OPT_STR,
    "start_location": LOCATION,
    "start_address": ADDRESS,
    "end_location": LOCATION,
    "end_address": ADDRESS,
    opt("path"): OPT_STR,
    opt("fuel_cost_usd"): OPT_FLOAT,
    opt("fuel_volume_l"): OPT_FLOAT,
    opt("average_kmpl"): OPT_FLOAT,
    opt("average_from_epa_kmpl"): OPT_FLOAT,
    opt("score_events"): OPT_FLOAT,
    opt("score_speeding"): OPT_FLOAT,
    opt("hard_brakes"): OPT_INT,
    opt("hard_accels"): OPT_INT,
    opt("duration_over_70_s"): OPT_INT,
    opt("duration_over_75_s"): OPT_INT,
    opt("duration_over_80_s"): OPT_INT,
    vol.Optional("vehicle_events", default=[]): [VEHICLE_EVENT],
    opt("start_timezone"): OPT_STR,
    opt("end_timezone"): OPT_STR,
    opt("city_fraction"): OPT_FLOAT,
    opt("highway_fraction"): OPT_FLOAT,
    opt("night_driving_fraction"): OPT_FLOAT,
    opt("idling_time_s"): OPT_INT,
    "tags": [str],
})
