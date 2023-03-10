"""
Weather station problem: temperatures in a linked list
@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729
"""

import pytest


class Node:
    def __init__(self, degrees: float, link=None):
        """Linked list node for temperature measurement.

        Parameters:
        ----------
        degrees: float,
            the temperature recorded in degrees (celsius).
        link: Node, default=None:
            the next node in the list, or None if final node.
        """
        self.degrees = degrees
        self.link = link


class TemperatureList:
    def __init__(self):
        """Initialize an empty linked list for temperature measurements."""
        self.root = None

    def insert(self, degrees: float):
        """Record a new measurement, inserting it at the beginning of the list.

        Parameters:
        ----------

        degrees: float,
            The degrees (celsius) recorded in the new entry to be added.

        Returns:
        --------
        self
            Returns the list object after the update. This way we can
            chain multiple calls, e.g.:
            `x = TemperatureList().insert(5.5).insert(6)`
        """
        new_root = Node(degrees, link=self.root)
        self.root = new_root

        # return self so we can chain multiple calls
        return self


# candidate functions


def get_highest_temperature_v1(lst):
    """Attempt by developer #1"""

    if lst.root is None:  # if empty list
        return None

    highest_temperature = 0
    node = lst.root

    while node is not None:
        if node.degrees > highest_temperature:
            highest_temperature = node.degrees

        node = node.link

    return highest_temperature


def get_highest_temperature_v2(lst):
    """Attempt by developer #2"""

    if lst.root is None:  # if empty list
        return None

    node = lst.root
    return_value = None

    while node is not None:
        highest_temperature = node.degrees
        node = node.link
        if node is not None and node.degrees > highest_temperature:
            return_value = node.degrees

    return return_value


def get_highest_temperature_v3(lst):
    """Attempt by developer #3"""

    def _recurse_max_temperature(node):
        if node.link is None:
            return node.degrees
        else:
            return max(node.degrees, _recurse_max_temperature(node.link))

    if lst.root is None:
        return None

    return _recurse_max_temperature(lst.root)


def get_highest_temperature_v4(lst):
    """Attempt by you"""

    if lst.root is None:  # if empty list
        return None

    node = lst.root
    # -459.67 is the lowest temperature possible in fahrenheit
    return_value = -460

    while node is not None:
        if node.degrees < return_value:
            break

        return_value = node.degrees
        node = node.link

    return return_value


funcs = [
    get_highest_temperature_v1,
    get_highest_temperature_v2,
    get_highest_temperature_v3,
    get_highest_temperature_v4,
]

# tests


@pytest.mark.parametrize("func", funcs)
def test_example_list(func):
    # build a list containing [20, 100, 8, 7] by inserting at beginning.
    temps = TemperatureList().insert(7).insert(8).insert(100).insert(20)

    res = func(temps)
    assert res == 100


# Add your own tests below


@pytest.mark.parametrize("func", funcs)
class TestParametrized:
    def test1(self, func):
        """
        Checks if the implementations return None when given an empty list
        """
        temps = TemperatureList()
        res = func(temps)
        assert res is None

    def test2(self, func):
        """
        Checks if the implementation work correctly when there are duplicates
        in the list
        """
        temps = TemperatureList().insert(100).insert(100)
        res = func(temps)
        assert res == 100

    def test3(self, func):
        """
        Checks if the implementaitons work correctly when there is only one
        element in the list
        """
        temps = TemperatureList().insert(200)
        res = func(temps)
        assert res == 200

    def test4(self, func):
        """
        Checks if the implementations work correctly when the highest
        temperature is the first element of the list
        """
        temps = TemperatureList().insert(100).insert(200).insert(300)
        res = func(temps)
        assert res == 300

    def test5(self, func):
        """
        Checks if the implementations handle negative temperatures correctly
        """
        temps = TemperatureList().insert(-10).insert(-20).insert(-30)
        res = func(temps)
        assert res == -10

    def test6(self, func):
        """
        Checks if the implementaitons work correctly when the highest
        temperature is the last element of the list
        """
        temps = TemperatureList().insert(300).insert(200).insert(100)
        res = func(temps)
        assert res == 300

    def test7(self, func):
        """
        Checks if the implementations work correctly with increasing
        temperatures seperated by lower temperatures (for example
        [100, 10, 200])
        """
        temps = TemperatureList().insert(200).insert(10).insert(100)

        res = func(temps)
        assert res == 200


"""
From the output of the tests we can conclude that implementation 1 and 2 aren't
correct implementations of the given specifications.

implementaiton 1 fails on test 5, since it initilaizes it's return value at 0
and checks if other temperatures are larger than it. However, temperatures
can be negative, so this method doesn't work.

implementation 2 fails on test 2 through 4. These tests fail because a return
value only gets set when there is a value larger than the first value. If the
following values are smaller, equal or non existent, the return value
stays None.
"""

if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
