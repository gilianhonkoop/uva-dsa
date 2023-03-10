"""
Dictionary demo
@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729
"""

import os

import matplotlib.pyplot as plt
from dictionary import Dictionary


def populate_dictionary(dictionary, filename: str, separator: str = "|"):
    """Populate an empty dictionary with all words present in the given
    filename and defined separator and return it again.
    """
    with open(filename, "r") as file:
        for line in file:
            lan1, lan2 = line.split(separator)
            dictionary[lan1.strip()] = lan2.strip()

    return dictionary


def plot_bucket_occupancy(dictionary):
    """Plot the bucket occupancy graph for a given dictionary. Matplotlib can
    be used to create the graph."""
    x = range(dictionary.n_buckets)
    y = dictionary.bucket_sizes()

    plt.bar(x, y)
    plt.xticks(x, range(dictionary.n_buckets))
    plt.show()


def main():
    # Initialize an empty dictionary
    nl_en_dict_builtin = {}
    nl_en_dict_custom = Dictionary()

    # Adjust this to the correct location of your dictionary
    file = os.path.join("./", "nl-en-dict.txt")

    # Populate dictionay
    nl_en_dict_builtin = populate_dictionary(nl_en_dict_builtin, file)
    nl_en_dict_custom = populate_dictionary(nl_en_dict_custom, file)

    # Test queries
    word1 = "woordenboek"
    word2 = "kat"
    word3 = "algoritme"

    print("Built-in dictionary results:")
    for w in (word1, word2, word3):
        print("The dutch word", w, "is translated as", nl_en_dict_builtin[w])

    print("\nCustom dictionary results:")
    for w in (word1, word2, word3):
        print("The dutch word", w, "is translated as", nl_en_dict_custom[w])

    en_nl_dict_custom = nl_en_dict_custom.invert()

    word4 = "dictionary"
    word5 = "cat"
    word6 = "algorithm"

    print("\nCustom dictionary inverted results:")
    for w in (word4, word5, word6):
        print(
            "The english word",
            w,
            "is translated as",
            en_nl_dict_custom[w],
        )

    plot_bucket_occupancy(nl_en_dict_custom)


if __name__ == "__main__":
    main()
