import asyncio
from typing import List, Dict, Any
from src.modules.base_module import BaseModule
from rich.console import Console

console = Console()


class OSINTEngine:
    def __init__(self):
        self.modules: List[BaseModule] = []
        self.results: Dict[str, Any] = {}

    def register_module(self, module: BaseModule) -> None:
        self.modules.append(module)

    async def scan(self, phone_number: str) -> Dict[str, Any]:
        console.print(f"[bold blue][*][/bold blue] Avvio scansione per: {phone_number}")

        # Esecuzione parallela di tutti i moduli caricati
        tasks = [module.run(phone_number) for module in self.modules]
        completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(completed_tasks):
            module_name = self.modules[i].name
            if isinstance(result, Exception):
                console.print(f"[red][!] Errore nel modulo {module_name}: {result}[/red]")
                self.results[module_name] = {"status": "error", "message": str(result)}
            else:
                self.results[module_name] = result

        return self.results