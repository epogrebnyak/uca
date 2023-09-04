from uca.extract import contains_uppercase_word


def test_contains_uppercase_word_positive():
    assert contains_uppercase_word(
        "GOAL SETTING Ability to set appropriate and realistic goals"
    )


def test_contains_uppercase_word_negative():
    assert not contains_uppercase_word("WFT is AI?", 4)
