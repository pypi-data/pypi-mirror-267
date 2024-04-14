import pytest

from json import loads
from pathlib import Path
from m_car_api.objects import APIReturn, VehicleReturn, parse_vehicles_payload


@pytest.fixture(scope="session")
def vehicle_json_path() -> Path:
    return Path(__file__).parent / "vehicle_return.json"


@pytest.fixture(scope="session")
def vehicle_json(vehicle_json_path: str) -> str:
    with open(vehicle_json_path) as f:
        return f.read()


def test_vehicle_check(vehicle_json: str):
    result = parse_vehicles_payload(loads(vehicle_json))
    assert isinstance(result, APIReturn[VehicleReturn])
    first_vehicle = result.data.vehicles[0]
    first_vehicle.id == 10326
    first_vehicle.license_plate == "B-MS 4309"
