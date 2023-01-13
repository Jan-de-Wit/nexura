from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def generateImplications(knight, knave, sentence):
    """ 
    Generates the implications for the given sentence. 
    Inspired by a comment made by user @m_smg on reddit:
    https://www.reddit.com/r/cs50/comments/iepghj/hello_can_any_body_explain_me_how_to_solve_the/
    """

    implications = And()

    implications.add(Implication(knight, sentence))
    implications.add(Implication(knave, Not(sentence)))

    return implications


baseRules = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    baseRules,
    generateImplications(AKnight, AKnave, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    baseRules,
    generateImplications(AKnight, AKnave, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    baseRules,
    generateImplications(AKnight, AKnave, Or(
        And(AKnave, BKnave), And(AKnight, BKnight))),
    generateImplications(BKnight, BKnave, Or(
        And(AKnight, BKnave), And(AKnave, BKnight))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    baseRules,
    Implication(AKnight, Or(AKnight, AKnave)),
    generateImplications(BKnight, BKnave, Implication(AKnight, BKnave)),
    generateImplications(BKnight, BKnave, CKnave),
    generateImplications(CKnight, CKnave, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
