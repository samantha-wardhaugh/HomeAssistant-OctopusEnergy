import pytest
from datetime import datetime
from custom_components.octopus_energy import api_client

@pytest.mark.parametrize("half_hourly_offset, current_time, expected_value",[
  (0, datetime(2023, 1, 1, 10, 0), True),
  (0, datetime(2023, 1, 1, 10, 30), True),
  (0, datetime(2023, 1, 1, 10, 29), False),
  (0, datetime(2023, 1, 1, 10, 29), False),
  (0, datetime(2023, 1, 1, 10, 3), False),
  (0, datetime(2023, 1, 1, 10, 33), False),
  (0, datetime(2023, 1, 1, 10, 17), False),
  (0, datetime(2023, 1, 1, 10, 47), False),
  (29, datetime(2023, 1, 1, 10, 0), False),
  (29, datetime(2023, 1, 1, 10, 30), False),
  (29, datetime(2023, 1, 1, 10, 29), True),
  (29, datetime(2023, 1, 1, 10, 29), True),
  (29, datetime(2023, 1, 1, 10, 3), False),
  (29, datetime(2023, 1, 1, 10, 33), False),
  (29, datetime(2023, 1, 1, 10, 17), False),
  (29, datetime(2023, 1, 1, 10, 47), False),
  (3, datetime(2023, 1, 1, 10, 0), False),
  (3, datetime(2023, 1, 1, 10, 30), False),
  (3, datetime(2023, 1, 1, 10, 29), False),
  (3, datetime(2023, 1, 1, 10, 29), False),
  (3, datetime(2023, 1, 1, 10, 3), True),
  (3, datetime(2023, 1, 1, 10, 33), True),
  (3, datetime(2023, 1, 1, 10, 17), False),
  (3, datetime(2023, 1, 1, 10, 47), False),
  (17, datetime(2023, 1, 1, 10, 0), False),
  (17, datetime(2023, 1, 1, 10, 30), False),
  (17, datetime(2023, 1, 1, 10, 29), False),
  (17, datetime(2023, 1, 1, 10, 29), False),
  (17, datetime(2023, 1, 1, 10, 3), False),
  (17, datetime(2023, 1, 1, 10, 33), False),
  (17, datetime(2023, 1, 1, 10, 17), True),
  (17, datetime(2023, 1, 1, 10, 47), True),
])
def test_is_time_for_half_hourly_call(half_hourly_offset: int, current_time: datetime, expected_value: bool):
  client = api_client.OctopusEnergyApiClient("NOT_REAL")
  client.half_hourly_offset = half_hourly_offset

  actual_value = client.is_time_for_half_hourly_call(current_time)

  assert actual_value == expected_value
