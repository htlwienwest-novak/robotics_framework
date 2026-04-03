# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
#  pip install rich
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os
from rich.live import Live
from rich.table import Table

mb = TelemetryBroker()

vel_dict = {"vel_linear_x":0, "vel_angular_z":0, "tool_pen":0, "led_blink":0}

table = Table()
table.add_column("Key")
table.add_column("Value")

with Live(table, refresh_per_second=20) as live:
    while True:
        try:
            table = Table(show_header=False, show_lines=True, padding=(0, 1, 0, 1), box=None)
            data = mb.getall()
            table.add_row("ACTIVE NODES:", style="bold green")

            for key, value in sorted(data.items()):
                if key.startswith("node_") or key.startswith("_node_"):
                    table.add_row(key, style="green")

            table.add_row("ACTIVE DATA:", style="bold")

            for key, value in sorted(data.items()):
                if not key.startswith("node_") and not key.startswith("_node_"):
                    table.add_row(key, str(value))
            
            live.update(table)

        except KeyboardInterrupt:
            break


