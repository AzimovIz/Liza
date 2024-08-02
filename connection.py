from dataclasses import dataclass
from typing import List

@dataclass
class Connection:
    sender: str
    allowed_purposes: List[str]
    acceptors: List[str]