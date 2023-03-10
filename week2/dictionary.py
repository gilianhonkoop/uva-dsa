"""
Dictionary demo
@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729
"""

from __future__ import annotations
import warnings


class Word:
    def __init__(self, key: str, value, link):
        self.key = key
        self.value = value
        self.link = link


class Bucket:
    def __init__(self):
        """Initialize an empty bucket."""
        self.root = None
        self.__len__ = 0

    def lookup(self, key: str):
        """Find the correct key and return the word. If the key cannot be
        found raise a KeyError."""
        curr = self.root

        while curr is not None:
            if curr.key == key:
                return curr

            curr = curr.link

        raise KeyError("Key can not be found")

    def insert(self, key: str, value):
        """Insert a word into the bucket. If the key doesn't exists create a
        new word. If they key already exists only update its value."""
        curr = self.root

        if curr is None:
            self.root = Word(key, value, None)
            self.__len__ = 1
            return

        while True:
            if curr.key == key:
                curr.value = value
                return

            if curr.link is None:
                curr.link = Word(key, value, None)
                self.__len__ += 1
                return

            curr = curr.link

    def delete(self, key: str):
        """Delete the given key from the bucket or raise a KeyError if the
        word cannot be found."""
        curr = self.root
        prev = None

        if curr is None:
            raise KeyError("Key can not be found")

        if curr.key == key:
            self.root = curr.link
            self.__len__ == 0
            return

        while curr is not None:
            if curr.key == key:
                prev.link = curr.link
                self.__len__ -= 1
                return

            prev = curr
            curr = curr.link

        raise KeyError("Key can not be found")

    def __len__(self):
        """Return the number of words in the bucket."""
        return self.__len__


class Dictionary:
    def __init__(self, n_buckets: int = 20):
        self.n_buckets = n_buckets
        self._ht = [Bucket() for _ in range(n_buckets)]

    def bucket_sizes(self):
        """List of bucket sizes"""
        return [len(bucket) for bucket in self._ht]

    def load_factor(self):
        """Return the load factor alpha of the dictionary"""
        return sum(self.bucket_sizes()) / self.n_buckets

    def _hash_first(self, key: str):
        """Hash the given string to a number between [0, n_buckets) using the
        character value of the first character"""
        if not isinstance(key, str):
            raise ValueError("Our dictionary only supports string keys.")
        return (ord(key[0]) if key else 0) % self.n_buckets

    def _hash_length(self, key: str):
        """Hash the given string to a number between [0, n_buckets) using the
        length of the word"""
        if not isinstance(key, str):
            raise ValueError("Our dictionary only supports string keys.")
        return len(key) % self.n_buckets

    def _hash_sum(self, key: str):
        """Hash the given string to a number between [0, n_buckets) using the
        sum of the character values in the word"""
        if not isinstance(key, str):
            raise ValueError("Our dictionary only supports string keys.")
        return (
            (sum([ord(letter) for letter in key]) % self.n_buckets)
            if key
            else 0
        )

    # change this to select a different hash function
    _hash = _hash_length

    def update(self, key: str, value):
        """Set the value associated with the given key."""
        bucket = self._ht[self._hash(key)]

        bucket.insert(key, value)

    def lookup(self, key: str):
        """Return the value associated with the given key."""
        bucket = self._ht[self._hash(key)]

        return bucket.lookup(key).value

    def delete(self, key: str):
        """Remove key from dictionary."""
        bucket = self._ht[self._hash(key)]

        bucket.delete(key)

    def invert(self) -> Dictionary:
        """Return a new dictionary where all key-value pairs are inverted,
        such that the old values are the new keys, and viceversa.
        If some of the values are equal, only one of the values will become
        a key in the inverted dictionary (can be anyone). In this case,
        `invert` must throw a warning printing the number of discarded pairs.
        """
        dictionary = Dictionary(self.n_buckets)

        for bucket in self._ht:
            curr = bucket.root

            while curr is not None:
                dictionary.update(curr.value, curr.key)
                curr = curr.link

        lost_pairs = (
            len(self) - len(dictionary) if len(self) > len(dictionary) else 0
        )

        warnings.warn(str(lost_pairs) + " pairs will be lost")

        return dictionary

    # the following definitions permit our custom dictionary
    # to mimic a builtin python dictionary.

    def __getitem__(self, key: str):
        return self.lookup(key)

    def __setitem__(self, key: str, value):
        return self.update(key, value)

    def __delitem__(self, key: str):
        return self.delete(key)

    def __len__(self):
        return sum([len(bucket) for bucket in self._ht])


if __name__ == "__main__":
    dict1 = Dictionary()
    dict1.update("woordenboek", "dictionary")
    print(dict1.lookup("woordenboek"))
    print(len(dict1))
