from validation import validate_text
from env.Roles.Checker import Checker
from env.Roles.Creator import Creator
from env.Roles.Maker import Maker

roles = [Checker(), Creator(), Maker()]

"""
    Role("test", ""),
    Role("realize", ""),
"""


def role(name):
    validate_text(name)
    for element in roles:
        if element.name() == name:
            return element
    return None
