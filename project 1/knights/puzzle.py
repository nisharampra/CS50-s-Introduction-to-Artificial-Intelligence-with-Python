from logic import *

# Define symbols for each character being a knight or knave
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a knight, then the sentence is true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a knave, then the sentence is false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A says "same kind"
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # B says "different kinds"
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave." but we don't know which
# B says "A said 'I am a knave.'"
# B then says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A says something: either "I am a knight" or "I am a knave"
    # B claims A said "I am a knave"
    # If B is a knight, then A said "I am a knave" -> A is saying AKnave
    Implication(BKnight, Biconditional(AKnight, AKnave)),

    # B also says "C is a knave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says "A is a knight"
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


# List of all puzzles
puzzles = [
    ("Puzzle 0", knowledge0),
    ("Puzzle 1", knowledge1),
    ("Puzzle 2", knowledge2),
    ("Puzzle 3", knowledge3)
]

# Run model checking for each puzzle
for puzzle_name, knowledge in puzzles:
    print(puzzle_name)
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"    {symbol}")
