"""
Sort a Python List

@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729

"""

from typing import List
from dataclasses import dataclass


# dataclasses are a convenient new way to create simple "structs" or "records"
# in Python.
@dataclass
class Product:
    name: str
    price: float


# hint: lst is a python list, so use lst[i] to access element i
# (=what we called "get" in class), and use len(lst) to get its size.


def sort_insertion(lst: List[Product]) -> List[Product]:
    """Sort lst by insertion, in-place."""
    for i in range(1, len(lst)):
        while i != 0 and lst[i].price < lst[i - 1].price:
            temp = lst[i - 1]
            lst[i - 1] = lst[i]
            lst[i] = temp
            i -= 1

    return lst


def merge(lst_a: List[Product], lst_b: List[Product]) -> List[Product]:
    """Given sorted lists lst_a and lst_b, combine them into a new sorted
    list."""
    combined = []
    a_len = len(lst_a)
    b_len = len(lst_b)

    ia = ib = 0

    while ia < a_len and ib < b_len:
        if lst_a[ia].price <= lst_b[ib].price:
            combined.append(lst_a[ia])
            ia += 1
        else:
            combined.append(lst_b[ib])
            ib += 1

    while ia < a_len:
        combined.append(lst_a[ia])
        ia += 1

    while ib < b_len:
        combined.append(lst_b[ib])
        ib += 1

    return combined


def sort_merge(lst: List[Product]) -> List[Product]:
    """Sort lst by merge sort. Leave the input list untouched.

    Since merge sort is not in-place, leave the input list unmodified.
    """
    n = len(lst)

    if n <= 1:
        return lst

    m = n // 2
    a = sort_merge(lst[:m])
    b = sort_merge(lst[m:])

    return merge(a, b)


def _partition_lomuto(lst: List[Product], p: int, r: int) -> int:
    """Lomuto partitioning of sublist lst[p:r] (including p, excluding r).
    Use the last element as pivot.

    Return the index of the pivot after permutations.
    """
    x = lst[r - 1].price
    i = p

    for j in range(p, r - 1):
        if lst[j].price <= x:
            temp = lst[i]
            lst[i] = lst[j]
            lst[j] = temp
            i += 1

    temp = lst[i]
    lst[i] = lst[r - 1]
    lst[r - 1] = temp

    return i


def _partition_hoare(lst: List[Product], p: int, r: int) -> int:
    """Hoare partitioning of sublist lst[p:r] (including p, excluding r).
    Use the middle element as pivot. (if even length, take the "floor").

    Return the index of the pivot after permutations.
    """
    x = lst[(p + r - 1) // 2].price
    i = p - 1
    j = r

    while True:
        while True:
            i += 1
            if lst[i].price >= x:
                break

        while True:
            j -= 1
            if lst[j].price <= x:
                break

        if i >= j:
            break

        temp = lst[i]
        lst[i] = lst[j]
        lst[j] = temp

    return j


def _quicksort_recurse_lomuto(lst: List[Product], p: int, r: int) -> None:
    """Quicksort recursion: sort lst[p:r] (including p, excluding r).

    Use the Lomuto partitioning strategy and recursion, as in class:
    recurse into lst[p:q] and lst[q+1:r].

    Do not return anything, change lst in place.

    (internal function)
    """
    if r - p > 1:
        pivot = _partition_lomuto(lst, p, r)
        _quicksort_recurse_lomuto(lst, p, pivot)
        _quicksort_recurse_lomuto(lst, pivot + 1, r)


def _quicksort_recurse_hoare(lst: List[Product], p: int, r: int) -> None:
    """Quicksort recursion: sort lst[p:r] (including p, excluding r).

    Use the Hoare partitioning strategy and recursion:
    recurse into lst[p:q+1] and lst[q+1:r].

    Do not return anything, change lst in place.

    (internal function)
    """
    if r - p > 1:
        pivot = _partition_hoare(lst, p, r)
        _quicksort_recurse_hoare(lst, p, pivot + 1)
        _quicksort_recurse_hoare(lst, pivot + 1, r)


def sort_quick_lomuto(lst: List[Product]) -> List[Product]:
    """Sort lst by in-place quick sort using the Lomuto scheme."""
    _quicksort_recurse_lomuto(lst, 0, len(lst))

    return lst


def sort_quick_hoare(lst: List[Product]) -> List[Product]:
    """Sort lst by in-place quick sort using the Hoare scheme."""
    _quicksort_recurse_hoare(lst, 0, len(lst))

    return lst


def main():
    sample_inventory = [
        Product(name="banana", price=5.99),
        Product(name="peanut butter", price=3),
        Product(name="jelly", price=3),
        Product(name="Little Oblivions CD", price=12),
        Product(name="guitar strings", price=4.20),
    ]

    print("original list")
    print(sample_inventory)

    # Python built-in sort: use lambda-expression to select the sort key.
    print("built-in sort")
    print(sorted(sample_inventory, key=lambda x: x.price))

    # insertion sort
    print("insertion sort")
    # since insertion sort is in place, we first make a copy of the inventory,
    # so that we can keep testing other sorting algos afterward.
    sample_inv_copy = sample_inventory.copy()
    print(sort_insertion(sample_inv_copy))

    # merge sort
    print("merge sort")
    print(sort_merge(sample_inventory))

    # quick sort
    print("quick sort")
    # since quicksort is in place, we make a copy.
    sample_inv_copy = sample_inventory.copy()
    print(sort_quick_lomuto(sample_inv_copy))

    # quick sort alternative partitioning
    print("quick sort (Hoare)")
    # since quicksort is in place, we make a copy.
    sample_inv_copy = sample_inventory.copy()
    print(sort_quick_hoare(sample_inv_copy))


if __name__ == "__main__":
    main()
