import pytest
from packaging_demo.states_info import is_city_capitol_of_state


@pytest.mark.parametrize(
    argnames="city_name, state, is_capitol",
    argvalues=[
        ("Montgomery", "Alabama", True),
        ("Juneau", "Alaska", True),
        ("Juneau", "Alabama", False),
        ("", "", False),
    ],
)
def test__is_city_capitol_of_state__for_correct_city(city_name: str, state: str, is_capitol: bool):
    assert is_city_capitol_of_state(city_name=city_name, state=state) == is_capitol
