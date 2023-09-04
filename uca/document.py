from typing import List, Tuple, Dict
from yaml import safe_load as read_yaml
from dataclasses import dataclass


@dataclass
class Skill:
    title: str
    definition: str

    def __str__(self):
        if self.definition:
            return f"{self.title}: {self.definition}"
        return self.title


def skill(text: str | Dict) -> Skill:
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


@dataclass
class DictDocument:
    data: dict

    def stream(self) -> Tuple[str, List[Skill]]:
        return [
            (title, [skill(t) for t in terms]) for title, terms in self.data.items()
        ]


@dataclass
class TextDocument:
    text: str

    def stream(self) -> Tuple[str, List[Skill]]:
        return DictDocument(data=read_yaml(self.text)).stream()
