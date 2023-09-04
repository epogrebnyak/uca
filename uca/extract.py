from yaml import safe_load_all as read_yamls  # type: ignore
from typing import Dict, Tuple

from uca.main import Skill, Node, Section
from uca.document import DictDocument


def contains_uppercase_word(text: str, min_length: int = 4) -> bool:
    for word in text.split():
        if len(word) >= min_length and word.isupper():
            return True
    return False


def extract_skill(text: str | Dict) -> Skill:
    if isinstance(text, dict):
        skill_name = list(text.keys())[0]
        definition = list(text.values())[0]
    if isinstance(text, str):
        if "~" in text:
            parts = text.split("~")
            skill_name = parts[0].strip()
            definition = parts[1].strip()
        else:
            skill_name = text
            definition = ""
    skill_name = skill_name.capitalize()
    definition = definition.capitalize()
    return Skill(skill_name, definition)


def extract_node(doc: str) -> Tuple[str, Node]:
    """
    Extract section, subsections and skills from *doc* and create a new node.

    The *doc* string should look like below, title and shorthand are mandatory.

    title: Personal and emotional skills
    shorthand: PE
    ---
    Subsection 1:
    - term A
    - term B ~ Definition
    Subsection 2:
    - term C ~ Other definition
    - term D
    - term E
    """
    section, content = list(read_yamls(doc))
    title = section["title"]
    shorthand = section["shorthand"]
    node = Node(Section(title, shorthand))
    for k, (topic, skills) in enumerate(DictDocument(content).stream()):
        tag = shorthand + str(k + 1)
        node.add_section(topic, tag)
        for skill in skills:
            node[tag].add_skill(skill.title, skill.definition)
    return shorthand, node
