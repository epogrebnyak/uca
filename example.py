from uca.main import Node, String, Viewer

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
- Emotional control
"""
skillset.add_document(doc1)
Viewer(skillset).print()
