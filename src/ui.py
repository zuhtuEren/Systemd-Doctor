import json, os, socket, platform
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from InquirerPy import inquirer

console = Console()

def display_system_dashboard(summary_data):
    if not summary_data: return
    grid = Table.grid(padding=(0, 1))
    grid.add_column(style="bold cyan"); grid.add_column(style="white")
    grid.add_row("Boot Summary:", summary_data['boot_summary'])
    grid.add_row("Active Services:", f"[yellow]{summary_data['active_services']}[/]")
    grid.add_row("Hostname:", socket.gethostname())
    grid.add_row("Kernel:", platform.release())
    console.print("\n", Panel(grid, title="[bold white]SYSTEMD-DOCTOR DASHBOARD[/bold white]", title_align="left", border_style="blue", padding=(1, 2), expand=False, box=box.ROUNDED))

def display_blame_table(services):
    table = Table(title="Systemd-Doctor: Boot Analysis", title_style="bold cyan", show_lines=True)
    table.add_column("Risk", justify="center", style="bold", width=6)
    table.add_column("Service Name", style="white", width=30)
    table.add_column("Time", style="magenta", width=12)
    table.add_column("Note / Description", style="green")
    
    colors = {1: "[green]1[/]", 2: "[cyan]2[/]", 3: "[yellow]3[/]", 4: "[orange1]4[/]", 5: "[red]5[/]"}
    for s in services:
        note_display = s['note']
        if "[USER]" in note_display:
            note_display = note_display.replace("[USER]", "[bold magenta][USER RULE][/bold magenta]")
        elif s['note'] == s['name'] or s['note'] == "No description.":
            note_display = f"[italic white]{s['name']}[/] (System Description)"
        table.add_row(colors.get(s['risk'], "3"), s['name'], s['time'], note_display)
    console.print(table)

def interactive_restore_menu(snapshots):
    if not snapshots:
        return None
    choices = [{"name": os.path.basename(s), "value": s} for s in snapshots[:10]]
    return inquirer.select(message="Select a snapshot to restore:", choices=choices).execute()

def interactive_selection_menu(services):
    choices = [{"name": f"{s['name']} ({s['time']})", "value": s['name']} for s in services]
    return inquirer.checkbox(message="Select units to disable:", choices=choices).execute()

def display_performance_report(saved_ms, unit_count):
    saved_sec = saved_ms / 1000
    mood = "[bold green]Success![/]" if saved_sec > 0.5 else "[bold cyan]Optimization complete.[/]"
    grid = Table.grid(padding=(0, 1))
    grid.add_row("[bold]Units Optimized:[/]", f"[cyan]{unit_count}[/]")
    grid.add_row("[bold]Time Saved:[/]", f"[bold yellow]{saved_sec:.3f}s[/]")
    grid.add_row("", ""); grid.add_row(mood, "")
    console.print("\n", Panel(grid, title="[bold green]OPTIMIZATION REPORT[/bold green]", border_style="green", padding=(1, 2), expand=False, box=box.ROUNDED))

def display_history(snaps):
    if not snaps:
        console.print("[yellow]No history found.[/yellow]")
        return
    table = Table(title="Action History", title_style="bold yellow", show_lines=True)
    table.add_column("File"); table.add_column("Date"); table.add_column("Saved Time")
    for f_p in snaps:
        try:
            with open(f_p, 'r') as f:
                d = json.load(f); m = d.get("metadata", {})
                table.add_row(os.path.basename(f_p), m.get("timestamp"), f"{m.get('saved_ms', 0)/1000:.3f}s")
        except: continue
    console.print(table)

def show_dependency_warning(analysis_map):
    table = Table(title="RELATIONSHIP WARNING", show_lines=True)
    table.add_column("Target"); table.add_column("Related Unit"); table.add_column("Type")
    for s, info in analysis_map.items():
        for d in info['deps']: table.add_row(s, d, "Required By")
        for t in info['triggers']: table.add_row(s, t, "Trigger")
    console.print(table)
    return inquirer.confirm(message="Proceed with changes?", default=False).execute()

def show_final_confirmation(final_list):
    console.print("\n[bold yellow]FINAL OPERATION LIST[/bold yellow]")
    for unit in final_list: console.print(f" - {unit}")
    return inquirer.confirm(message="Confirm execution?", default=True).execute()