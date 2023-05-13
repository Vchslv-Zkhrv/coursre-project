from dataclasses import dataclass
from typing import Literal


user_group = Literal["owner", "admin", "user"]


@dataclass
class User():
    login: str
    group: user_group
    last_proj: str
