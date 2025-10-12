#!/usr/bin/env python3
# system_health.py
# Purpose: Check CPU, memory, and disk usage

import psutil
import socket
import smtplib
from email.mime.text import MIMEText

CPU_THRESHOLD = 85
MEM_THRESHOLD = 80
DISK_THRESHOLD = 90
EMAIL = "ops-team@example.com"

def check_system():
    alerts = []
    hostname = socket.gethostname()

    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        alerts.append(f"High CPU usage: {cpu}%")

    mem = psutil.virtual_memory().percent
    if mem > MEM_THRESHOLD:
        alerts.append(f"High memory usage: {mem}%")

    disk = psutil.disk_usage('/').percent
    if disk > DISK_THRESHOLD:
        alerts.append(f"Disk nearly full: {disk}%")

    if alerts:
        send_alert(hostname, alerts)

def send_alert(hostname, alerts):
    msg = MIMEText("\n".join(alerts))
    msg["Subject"] = f"[ALERT] System Health Warning on {hostname}"
    msg["From"] = "monitor@local"
    msg["To"] = EMAIL

    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()

if __name__ == "__main__":
    check_system()