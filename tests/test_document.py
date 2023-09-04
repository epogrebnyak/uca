from uca.document import skill, Skill, TextDocument


def test_skill():
    assert skill({"term C": "Another definition"}) == Skill(
        "Term c", "Another definition"
    )


def test_TextDocument_stream():
    assert (
        TextDocument(
            """
Subsection 1:
    - term A
    - term B ~ Definition
Subsection 2:
    - term C: Another definition
    - term D
    - term E
"""
        ).stream()
        == [
            (
                "Subsection 1",
                [
                    Skill(title="Term a", definition=""),
                    Skill(title="Term b", definition="Definition"),
                ],
            ),
            (
                "Subsection 2",
                [
                    Skill(title="Term c", definition="Another definition"),
                    Skill(title="Term d", definition=""),
                    Skill(title="Term e", definition=""),
                ],
            ),
        ]
    )
