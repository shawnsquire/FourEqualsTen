#!/usr/bin/env python

# Pull the product function from itertools to make permutation generation with repeats
# We will use the chain to combine with zipping for later
from itertools import product, chain

# Target value to hit
TARGET = 10

# List of every digit to permutate
DIGITS = range(0, 10)
# Number of digits to have per challenge
CHALLENGE_LENGTH = 4

# All possible positions of parentheses
# 0 indexed from the left-most blank spot
# E.g., (2, 4) is A B ( C D )
#                0 1 *2* 3 *4*
# We don't need parentheses around the entire set
# Nor do we need parentheses around a single number
PAREN_POSITIONS = [
    (),     # A B C D
    (0, 2), # (A B) C D
    (0, 3), # (A B C) D
    (1, 3), # A (B C) D
    (1, 4), # A (B C D)
    (2, 4)  # A B (C D)
]

# A set of all main operators, which translate to arithmetic functions
OPERATORS = [ '+', '-', '*', '/' ]

# Generate a full set of challenge number sets
# Order does not *truly* matter since numbers can be re-arranged
# However, we can check for solutions along the entire board
# We will check later to see if some are unsolvable with the existing layout
challenges = list(product(DIGITS, repeat=CHALLENGE_LENGTH))
print(len(challenges), "Possible permutations")

# Find an operator to stick between each number, and generate all possibilities
# We will deal with missing operators separately
# Due to fencepost problem, we want the number of digits in a challenge minus one
ops = list(product(OPERATORS, repeat=CHALLENGE_LENGTH-1))
print(len(ops), "Possible operator combinations")

# We'll define a few functions to make the next parts cleaner


# zip_formula takes a challenge as a list of values and an op as a set of operators to weave
# It will output a list of length CHALLENGE*2 - 1 that is structured such as:
# [ A ? B ? C ? D ] where ? is some operator
def zip_formula(challenge, op):
    # Due to how length of each array in zip must match but we know we have one more number
    # we can manually add this to the end after the zip
    return list(chain.from_iterable(zip(challenge, op))) + [challenge[-1]]


# eval_zipped_formula takes advantage of the eval function in python to do the math for us
# Given a z zipped formula (see zip_formula) we join it together and run eval
# This does all the work for our order of operations considerations for us!
# Note, that join expects ever value to be a string, so we must convert our digits to a string first
def eval_zipped_formula(z):
    try:
        return eval("".join([str(c) for c in z]))
    # Sometimes, we may get division by 0
    # Rather than try and catch this in advance (which is hard if there are no zeroes present; e.g., 1/(4-4))
    # we just let Python catch this problem for us and return false
    # Since False should never equal the target, we shouldn't have an issue
    except ZeroDivisionError:
        return False


# eval_formula is just a simplified version of zipping and evaluating a specific challenge and set of operators!
def eval_formula(challenge, op):
    return eval_zipped_formula(zip_formula(challenge, op))


# Iterate through each possible challenge and find all the operator combinations that equal the TARGET
solutions = {challenge: [ op for op in ops if eval_formula(challenge, op) == TARGET ] for challenge in challenges}
print(sum([1 if len(x) == 0 else 0 for x in solutions]), "Challenge without solutions")

# Key: The challenge as 4-tuple
# Result: The correct operations as a list (in order)

# Let's get some numbers from the user!
while True:
    ch_input = input("Enter the challenge numbers: ")
    ch_key = [int(x) for x in ch_input.split() if x.isdigit()]
    if len(ch_key) == CHALLENGE_LENGTH:
        for i, res in enumerate(solutions[tuple(ch_key)]):
            print("Solution", i+1, ":", res)
    else:
        print("Sorry, that's not a valid set of numbers...")
