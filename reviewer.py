import os
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
console = Console()

def review_code(code):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "model": "openai/gpt-oss-120b:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Please review this code and give feedback:\n\n{code}"
                }
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

console.print(Panel(Text("AI Code Reviewer", justify="center", style="bold cyan")))
console.print("\n[yellow]Choose input method:[/yellow]")
console.print("  [cyan]1[/cyan] - Paste code manually")
console.print("  [cyan]2[/cyan] - Load from file")
choice = input("\nEnter 1 or 2: ").strip()

if choice == "2":
    file_path = input("Enter file path (e.g. C:\\Users\\user\\test.py): ").strip()
    try:
        with open(file_path, "r") as f:
            code = f.read()
        console.print(f"\n[green]File loaded successfully![/green]")
    except FileNotFoundError:
        console.print(f"\n[red]File not found: {file_path}[/red]")
        exit()
else:
    console.print("\n[yellow]Paste your code below. When done, type 'END' on a new line:[/yellow]\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    code = "\n".join(lines)

console.print("\n[bold green]Reviewing your code...[/bold green]\n")

result = review_code(code)

md = Markdown(result)
console.print(Panel(md, title="[bold yellow]Code Review Results[/bold yellow]", border_style="blue"))