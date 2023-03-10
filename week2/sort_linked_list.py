"""
Sorting on Linked lists

@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729

"""

from __future__ import annotations
from typing import Optional


class Node:
    def __init__(self, degrees: float, link: Optional[Node] = None):
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
        self._root = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

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
        new_root = Node(degrees, link=self._root)
        self._root = new_root
        self._length += 1

        # return self so we can chain multiple calls
        return self

    def split_half(self) -> tuple[TemperatureList, TemperatureList]:
        """
        This function finds the middle two nodes of the current list (rounded
        downwards), sever the link between them, and create a new
        TemperatureList.
        """
        newlist = TemperatureList()
        curr = self._root
        i = 0

        # find middle node
        while i != (len(self) - 1) // 2:
            curr = curr.link
            i += 1

        # fill the second list
        newlist._root = curr.link
        newlist._length = len(self) - i - 1

        # cut self into the first list
        curr.link = None
        self._length = i + 1

        return (self, newlist)

    def __repr__(self):
        """Returns a printable representational string of the given object."""
        node = self._root
        out = "["
        while node is not None:
            out += str(node.degrees)
            if node.link is not None:
                out += ", "
            node = node.link
        out += "]"
        return out

    def sort_merge(self) -> TemperatureList:
        """Implementation of merge sort"""
        if len(self) <= 1:
            return self

        a, b = self.split_half()
        # print("Split halves", a, b)
        a = a.sort_merge()
        b = b.sort_merge()

        # print("Sorted halves", a, b)
        res = merge(a, b)
        self._root = res._root
        self._length = res._length
        return self


def merge(a: TemperatureList, b: TemperatureList) -> TemperatureList:
    """
    This function takes two TemperatureLists, assumed sorted, and merges them
    in-place, without creating new Nodes, just by changing the links.
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a

    curr_a = a._root
    curr_b = b._root

    final_list = TemperatureList()

    # set the root of the new list
    if curr_a.degrees <= curr_b.degrees:
        final_list._root = curr_a
        curr_a = curr_a.link
    else:
        final_list._root = curr_b
        curr_b = curr_b.link

    curr_final = final_list._root

    # add nodes from a or b until one list has all its nodes added
    while curr_a is not None and curr_b is not None:
        if curr_a.degrees <= curr_b.degrees:
            curr_final.link = curr_a
            curr_final = curr_final.link
            curr_a = curr_a.link
        else:
            curr_final.link = curr_b
            curr_final = curr_final.link
            curr_b = curr_b.link

    # add the remainder of list a
    while curr_a:
        curr_final.link = curr_a
        curr_final = curr_final.link
        curr_a = curr_a.link

    # add the remainder of list b
    while curr_b:
        curr_final.link = curr_b
        curr_final = curr_final.link
        curr_b = curr_b.link

    final_list._length = len(a) + len(b)

    return final_list


def main():
    temps = (
        TemperatureList()
        .insert(5.99)
        .insert(8.20)
        .insert(-3.9)
        .insert(12)
        .insert(4.20)
    )
    print("Input:", temps)
    temps = temps.sort_merge()
    print("Sorted:", temps)


if __name__ == "__main__":
    main()
