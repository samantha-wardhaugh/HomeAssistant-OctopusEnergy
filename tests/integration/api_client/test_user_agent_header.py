import mock
import pytest
from datetime import datetime, time

from custom_components.octopus_energy.api_client import OctopusEnergyApiClient
from custom_components.octopus_energy.api_client import IntelligentSettings

COMMON_ARGS = {
    "period_from": datetime(2023, 10, 10, 10, 10),
    "period_to": datetime(2023, 10, 10, 10, 10),
    "target_time": time(10, 10),
    "tariff_code": "E-1R-VAR-22-11-01-C"
}


@pytest.mark.asyncio
@mock.patch('custom_components.octopus_energy.api_client.aiohttp.ClientSession.post')
@mock.patch('custom_components.octopus_energy.api_client.aiohttp.ClientSession.get')
async def test_user_agent_header_always_included(mock_get, mock_post):
    """
    This test iterates through every function that makes an API call and ensures
    an identifying "User-Agent" header is passed.
    """
    client = OctopusEnergyApiClient(api_key="blah")

    # Then generate a list of all the methods on the client, selecting only those
    # that make API calls (which all start with 'async').
    method_list = [getattr(client, function_name) for function_name in dir(OctopusEnergyApiClient) if
                   callable(getattr(OctopusEnergyApiClient, function_name)) and str(function_name).startswith('async')]

    # We don't care about the actual return values of the API call, just the request
    # object, so mock out the helper function that handles the response.
    with mock.patch.object(client, "__async_read_response__") as read_response_fn:
        read_response_fn.return_value = "this_is_irrelevant"

        for method in method_list:
            args_dict = await _generate_default_variables(method)

            if method.__name__ == "async_get_intelligent_settings":
                await method.__func__(client, **args_dict)
            else:
                # The other functions that handle intelligent octopus functionality first make
                # a call from async_get_intelligent_settings and rely on the results,
                # so we mock it out. We skip the mocking for the function itself,
                # so we still know the User-Agent is set for it.
                with mock.patch.object(client, "async_get_intelligent_settings") as intelligent_settings:
                    intelligent_settings.return_value = IntelligentSettings(
                        smart_charge="blah",
                        charge_limit_weekday=1,
                        charge_limit_weekend=1,
                        ready_time_weekday=time(10, 10),
                        ready_time_weekend=time(10, 10),
                    )
                    await method.__func__(client, **args_dict)

            # The function might have been making a graphQL call (always POST)
            # or a REST call (always GET), so we need to check both sets of mocks
            assert mock_post.call_count > 0 or mock_get.call_count > 0
            request_mock = mock_post if mock_post.call_count > 0 else mock_get

            kwargs_list = request_mock.call_args_list[-1][1]
            assert "headers" in kwargs_list
            assert "User-Agent" in kwargs_list["headers"]
            assert kwargs_list["headers"]["User-Agent"] == "bottlecapdave-homeassistant-octopusenergy"

            mock_post.reset_mock()
            mock_get.reset_mock()


async def _generate_default_variables(method_function: object) -> dict[str, object]:
    arg_count = method_function.__code__.co_argcount
    variable_names = method_function.__code__.co_varnames
    args_dict = {}
    for arg in range(1, arg_count):
        args_dict[variable_names[arg]] = COMMON_ARGS.get(variable_names[arg], "default_value")
    return args_dict

