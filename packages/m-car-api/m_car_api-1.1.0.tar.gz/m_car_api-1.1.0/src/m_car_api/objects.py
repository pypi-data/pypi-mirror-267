# flake8: noqa: F401

from pydantic.version import VERSION

if VERSION.startswith("1."):
    from m_car_api.objects_pydantic_1 import (
        DeviceInfo,
        Vehicle,
        VehicleQuery,
        VehicleReturn,
        APIReturn,
        parse_vehicles_payload,
    )
else:
    from m_car_api.objects_pydantic_2 import (
        DeviceInfo,
        Vehicle,
        VehicleQuery,
        VehicleReturn,
        APIReturn,
        parse_vehicles_payload,
    )
