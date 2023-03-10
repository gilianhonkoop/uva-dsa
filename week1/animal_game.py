"""
Question tree animal game
@author: R.J. Both and Vlad Niculae

Gilian Honkoop 13710729
"""

import os
import pickle


class AnswerNode:
    def __init__(self, answer=None):
        self.answer = answer

    def traverse_depth(self):
        return 0


class QuestionNode(AnswerNode):
    def __init__(self, question=None, if_yes=None, if_no=None):
        self.question = question
        self.if_yes = if_yes
        self.if_no = if_no

    def traverse_size(self, leaves):
        for child in [self.if_yes, self.if_no]:
            if type(child) == AnswerNode:
                leaves.append(self)
            else:
                child.traverse_size(leaves)

    def traverse_depth(self):
        left_depth = self.if_yes.traverse_depth()
        right_depth = self.if_no.traverse_depth()
        return max(left_depth, right_depth) + 1


class KnowledgeBase:
    def __init__(self, root=None):
        self.root = root

    def size(self):
        leaves = []

        if not self.root:
            return len(leaves)

        self.root.traverse_size(leaves)

        return len(leaves)

    def depth(self):
        if not self.root:
            return 0

        return self.root.traverse_depth()


def initialize_kb() -> None:
    """Create the initial knowledge base and save it in a pickle file."""
    # Adjust or delete the next line of code.
    kb = KnowledgeBase()

    a1 = AnswerNode("Frog")
    a2 = AnswerNode("Pelican")
    a3 = AnswerNode("Dolphin")
    a4 = AnswerNode("Panther")
    a5 = AnswerNode("Mouse")

    q1 = QuestionNode("Is it furry?", a4, a3)
    q2 = QuestionNode("Does it fly?", a2, a1)
    q3 = QuestionNode("Bigger than a chair?", q1, a5)
    q4 = QuestionNode("Is it a mammal?", q3, q2)

    kb.root = q4

    # Code to save the KnowledgeBase kb to the kb.pkl file.
    with open("kb.pkl", "wb") as f:
        pickle.dump(kb, f)


def play(kb: KnowledgeBase) -> None:
    curr_node = kb.root

    while type(curr_node) == QuestionNode:
        prev_node = curr_node

        while True:
            answer = input(curr_node.question + "\n> ")

            if answer == "yes" or answer == "no":
                break
            else:
                print("please answer with 'yes' or 'no'")

        if answer.startswith("y"):
            answer = True
            curr_node = curr_node.if_yes
        else:
            answer = False
            curr_node = curr_node.if_no

    if type(curr_node) == AnswerNode:
        while True:
            correct = input(
                "My guess is: "
                + curr_node.answer
                + ". Did I guess correctly?\n> "
            )

            if correct == "yes" or correct == "no":
                break
            else:
                print("please answer with 'yes' or 'no'")

        if correct.startswith("y"):
            print("** I win :) **")
        else:
            print("** I lose :( **")

            animal = input("What was the animal you thought about?\n> ")
            question = input(
                "Enter a question with answer yes for "
                + animal
                + ", but no for "
                + curr_node.answer
                + ".\n> "
            )

            update_kb(kb, animal, question, prev_node, answer)

            print("Thank you.")


def update_kb(kb, animal, question, qnode, answer):
    temp_answer = qnode.if_yes

    if answer:
        qnode.if_yes = QuestionNode(question, AnswerNode(animal), temp_answer)
    else:
        qnode.if_no = QuestionNode(question, AnswerNode(animal), temp_answer)

    with open("kb.pkl", "wb") as f:
        pickle.dump(kb, f)


# Run the animal game. The code below doesn't have to be adjusted.
if __name__ == "__main__":
    if not os.path.exists("kb.pkl"):
        print("Knowledge base does not exist. Initializing.")
        initialize_kb()

    with open("kb.pkl", "rb") as f:
        kb = pickle.load(f)

    while True:
        print(kb.size())
        print(kb.depth())

        print("Welcome to the Animals game!\n")
        print(
            "The current number of animals by the knowledge base is "
            + str(kb.size())
            + "."
        )
        print(
            "I can guess your animal in at most "
            + str(kb.depth())
            + " questions.\n"
        )

        play(kb)
        answer = input("Play again? >")
        if answer.startswith("n"):
            break
