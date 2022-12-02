#!/usr/bin/env python

# Pull the product function from itertools to make permutation generation with repeats
# We will use the chain to combine with zipping for later
# Permutations comes later when we want to re-arrange the numbers
from itertools import product, chain, permutations

# Mode to play with.
# Phase 1 -> Don't rearrange
# Phase 2 -> Check rearrangements
PHASE = 2

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
print(sum([1 if len(x) == 0 else 0 for x in solutions.values()]), "Challenges without solutions")

# Key: The challenge as 4-tuple
# Result: The correct operations as a list (in order)


# Display and receive a prompt for the numbers
def prompt_numbers():
    ch_input = input("Enter the challenge numbers: ")
    return [int(x) for x in ch_input.split() if x.isdigit()]


# Let's get some numbers from the user!
while PHASE == 1:
    ch_key = prompt_numbers()

    # If we didn't put in 4 numbers, let's let the user skip it
    if len(ch_key) != CHALLENGE_LENGTH:
        print("Sorry, that's not a valid set of numbers...")
        continue

    # If we don't have any solutions attached, just let the user know
    if len(solutions[tuple(ch_key)]) == 0:
        print("> No solutions found!")
        continue

    # If there are solutions, iterate through and show them to the user
    for i, res in enumerate(solutions[tuple(ch_key)]):
        print("> Solution", i+1, ":", res)

# We want to know how many problems can be solved with re-arrangement
if PHASE == 2:
    # For each item in solution, we want to permute the numbers
    # We only store if there was no solution at first but there is now
    # We could remove duplicates in a future version; e.g., 9 9 6 5 is a permutation of 9 9 6 5 [the 9s are swapped]
    alts = {i: [list(j) for j in permutations(i) if len(solutions[j]) > 0] for i, v in solutions.items() if len(v) == 0}
    print(sum([1 if len(x) == 0 else 0 for x in alts.values()]), "Challenges can be solved with re-arranging")

while PHASE == 2:
    ch_key = prompt_numbers()

    # Make sure we had 4 numbers
    if len(ch_key) != CHALLENGE_LENGTH:
        print("Sorry, that's not a valid set of numbers...")
        continue

    # If we have a solution right now, let's just show the answers (like Phase 1)
    if len(solutions[tuple(ch_key)]) > 0:
        print(">> No Rearrangement Required")
        for i, res in enumerate(solutions[tuple(ch_key)]):
            print("> Solution", i+1, ":", res)
        continue

    # Let's iterate through possible permutations
    if len(alts[tuple(ch_key)]) == 0:
        print("Re-arranging would not help!")
        continue

    for alt_ch_key in alts[tuple(ch_key)]:
        print(">> Arrangement:", " ".join([str(y) for y in alt_ch_key]))
        for i, res in enumerate(solutions[tuple(alt_ch_key)]):
            print("> Solution", i+1, ":", res)
            solution_found = True
