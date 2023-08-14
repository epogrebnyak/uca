import pytest

from uca import Node, String, Viewer
from uca.main import get_skills, yield_lines, root_node


def test_root_node():
    assert root_node(title="ABC").content.text.startswith("ABC")


@pytest.fixture
def skillset():
    skillset = Node(content=String("Skillset Example"))
    doc1 = """
title: Personal and emotional skills
shorthand: PE
---
Positive attitudes:
- optimism ~ positive outlook and hopeful attitude towards the future.
- Self-efficacy ~ Belief in own's accomplishment.

Emotional regulation:
- Stress resistance ~ Capability to handle pressure and adversity.
- EMOTIONAL CONTROL
"""
    skillset.add_document(doc1)
    return skillset


def test_get_skills_length(skillset):
    skills = get_skills(skillset)
    assert len(skills) == 4


def test_get_skills_titles(skillset):
    skills = get_skills(skillset)
    skill_titles = [skill.title for skill in skills]
    assert skill_titles == [
        "Optimism",
        "Self-efficacy",
        "Stress resistance",
        "Emotional control",
    ]


def test_yield_lines(skillset):
    a = list(yield_lines(skillset, "", "--"))
    b = list(yield_lines(skillset, "", "--"))
    assert len(b) == len(a) == 8


def test_count_skill(skillset):
    assert Viewer(skillset).count_skills() == 4


def test_size_does_not_grow_after_function_calls(skillset):
    list(yield_lines(skillset, "", "--"))
    s1 = skillset.size()
    list(yield_lines(skillset, "", "--"))
    s2 = skillset.size()
    assert s1 == s2 == 8
