from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Dict, Any

console = Console()


def print_rich_table(data: Dict[str, Any]):
    """Formatta i risultati della scansione in una tabella elegante."""

    console.print(Panel.fit("[bold green]AegisPhone Scan Results[/bold green]", border_style="blue"))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Modulo", style="cyan", width=20)
    table.add_column("Risultati/Dettagli", style="white")

    for module_name, content in data.items():
        # Trasformiamo il dizionario/lista in una stringa leggibile
        formatted_content = ""
        if isinstance(content, dict):
            formatted_content = "\n".join([f"[yellow]{k}:[/yellow] {v}" for k, v in content.items()])
        elif isinstance(content, list):
            formatted_content = "\n".join([f"• {item}" for item in content])
        else:
            formatted_content = str(content)

        table.add_row(module_name, formatted_content)

    console.print(table)