from uca.main import root_node

skillset = root_node("Skillset Example")
skillset.add_document(
    """
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
)
skillset.viewer.print()
