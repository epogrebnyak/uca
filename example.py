from uca.main import root_node

# SkillSet has a dict of sections

# skillset = SkillSet(title="Skillset Example 2")
# skillset.sections["PE"] = Section(title="Personal and emotional skills")
# skillset.sections["PE"].add_document("""
#Positive attitudes:
#- Optimism ~ Positive outlook and hopeful attitude towards the future.
#- Self-efficacy ~ Belief in own's accomplishment.
#
#Emotional regulation:
#- Stress resistance ~ Capability to handle pressure and adversity.
#- Emotional control
#""")

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
