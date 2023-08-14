import importlib.metadata
from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple

from pydantic.dataclasses import dataclass
from yaml import safe_load_all as read_yamls  # type: ignore


def version(package_name="uca") -> str | None:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        print(f"{package_name} is not installed")


class Language(Enum):
    Russian = "ru"
    English = "en"


@dataclass
class Item:
    main: str
    alternatives: List[str]

    def __str__(self):
        return self.main


@dataclass
class Skill:
    title: str | Item
    definition: str | Item
    translations: Dict[Language, "Skill"] = field(default_factory=dict)

    def __str__(self):
        if self.definition:
            return f"{str(self.title)}: {self.definition}"
        return str(self.title)


@dataclass
class Section:
    title: str | Item
    shorthand: str

    def __str__(self):
        return f"{self.title} ({self.shorthand})"


@dataclass
class String:
    text: str

    def __str__(self):
        return self.text


NodeContent = String | Section | Skill


@dataclass
class Node:
    content: NodeContent  # string, section or skill
    children: Dict[str, "Node"] = field(default_factory=dict)

    def __getitem__(self, key: str) -> "Node":
        return self.children[key]

    def __setitem__(self, key: str, node):
        self.children[key] = node

    def add_section(self, title, shorthand):
        self[shorthand] = Node(content=Section(title, shorthand))

    def add_skill(self, title, definition):
        self[title] = Node(content=Skill(title, definition))

    def add_document(self, doc: str):
        shorthand, node = extract_node(doc)
        self[shorthand] = node

    def size(self):
        return len(list(walk(self)))

    @property
    def viewer(self):
        return Viewer(self)


def root_node(title: str) -> Node:
    date = datetime.now().date().isoformat()
    s = f"{title} (version {version()}, build date {date})"
    return Node(String(s))


def extract_skill(text: str) -> Skill:
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
    for k, (topic, terms) in enumerate(content.items()):
        tag = shorthand + str(k + 1)
        node.add_section(topic, tag)
        for _, term in enumerate(terms):
            skill = extract_skill(term)
            node[tag].add_skill(skill.title, skill.definition)
    return shorthand, node


def walk(node: Node):
    yield (node.content)
    for _, child in node.children.items():
        yield from walk(node=child)


def yield_lines(node: Node, offset="", delta="--"):
    yield (offset, str(node.content))
    for child in node.children.values():
        yield from yield_lines(child, offset + delta, delta)


def print_tree(node: Node, offset="", delta="  "):
    for offset, text in yield_lines(node, offset, delta):
        print(offset + text)


def get_skills(node):
    def choose_skill(x):
        return isinstance(x, Skill)

    return list(filter(choose_skill, walk(node)))


@dataclass
class Viewer:
    node: Node

    def print(self):
        print_tree(self.node)

    def count_skills(self):
        return len(get_skills(self.node))
