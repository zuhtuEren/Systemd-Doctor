import subprocess, json, os, platform, socket
from datetime import datetime

SNAPSHOT_DIR = "snapshots"

def parse_time_to_ms(t_str):
    try:
        if 'min' in t_str: return float(t_str.replace('min','')) * 60000
        if 'ms' in t_str: return float(t_str.replace('ms',''))
        if 's' in t_str: return float(t_str.replace('s','')) * 1000
        return 0
    except: return 0

def get_service_status(n):
    try:
        r = subprocess.run(['systemctl', 'is-enabled', n], capture_output=True, text=True)
        return r.stdout.strip()
    except: return 'unknown'

def check_dependencies(n):
    try:
        r = subprocess.run(['systemctl', 'list-dependencies', n, '--reverse', '--plain'], capture_output=True, text=True)
        deps = r.stdout.strip().split('\n')
        return [d.strip() for d in deps[1:] if d.strip().endswith(".service")]
    except: return []

def get_unit_triggers(n):
    try:
        r = subprocess.run(['systemctl', 'show', '-p', 'TriggeredBy', n], capture_output=True, text=True)
        return r.stdout.split('=')[1].strip().split() if "=" in r.stdout else []
    except: return []

def disable_selected_services(selected, all_s):
    from src.ui import show_dependency_warning, show_final_confirmation, display_performance_report
    total = list(selected); analysis = {}
    for n in selected:
        d, t = check_dependencies(n), get_unit_triggers(n)
        if d or t:
            analysis[n] = {"deps": d, "triggers": t}
            for tr in t: 
                if tr not in total: total.append(tr)
    if analysis and not show_dependency_warning(analysis): return
    if not show_final_confirmation(total): return
    saved_ms = sum(parse_time_to_ms(next((s['time'] for s in all_s if s['name'] == u), "0ms")) for u in total)
    pre_states = {s['name']: {"status": get_service_status(s['name']), "managed": s['name'] in total} for s in all_s}
    try:
        for n in total: subprocess.run(['sudo', 'systemctl', 'disable', '--now', n], check=True)
        if not os.path.exists(SNAPSHOT_DIR): os.makedirs(SNAPSHOT_DIR)
        boot = subprocess.run(['systemd-analyze'], capture_output=True, text=True).stdout.split('\n')[0].split('=')[-1].strip()
        data = {"metadata": {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "boot_time": boot, "managed_count": len(total), "saved_ms": saved_ms}, "services": pre_states}
        with open(f"{SNAPSHOT_DIR}/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f: json.dump(data, f, indent=4)
        display_performance_report(saved_ms, len(total))
    except: print("[ERROR] Operation failed. Please check sudo permissions.")

def restore_snapshot(target):
    if not target: return
    
    # Akilli yol kontrolü:
    # 1. Kullanicinin girdigi yolu direkt dene
    # 2. Olmazsa snapshots/ klasörü altinda dene
    actual_path = target
    if not os.path.exists(actual_path):
        actual_path = os.path.join(SNAPSHOT_DIR, target)

    if not os.path.exists(actual_path):
        print(f"[ERROR] Snapshot file not found: {target}")
        print(f"[*] Looked in: {os.getcwd()} and {os.path.join(os.getcwd(), SNAPSHOT_DIR)}")
        return

    try:
        with open(actual_path, 'r') as f:
            data = json.load(f)
            for unit, info in data["services"].items():
                if info.get("managed"):
                    cmd = 'enable' if info['status'] == 'enabled' else 'disable'
                    subprocess.run(['sudo', 'systemctl', cmd, unit], capture_output=True)
        print(f"[SUCCESS] System reverted to: {os.path.basename(actual_path)}")
    except Exception as e: 
        print(f"[ERROR] {e}")