from dataclasses import dataclass
from typing import Literal


user_group = Literal["owner", "admin", "user"]


action_name = Literal[
    "open file",
    "open folder",
    "open last",
    "undo",
    "redo",
]


@dataclass
class User():
    login: str
    group: user_group
    last_proj: str
