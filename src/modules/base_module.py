from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModule(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, phone_number: str) -> Dict[str, Any]:
        """Esegue la scansione specifica del modulo."""
        pass