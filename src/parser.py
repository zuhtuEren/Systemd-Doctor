import subprocess

def get_systemd_blame_data():
    try:
        result = subprocess.run(['systemd-analyze', 'blame'], capture_output=True, text=True, check=True)
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except: return []

def get_service_description(service_name):
    try:
        cmd = ['systemctl', 'show', service_name, '--property=Description']
        result = subprocess.run(cmd, capture_output=True, text=True)
        desc = result.stdout.split('=')[1].strip()
        return desc if desc and desc != "" else service_name
    except: return service_name

def get_system_summary():
    try:
        analyze = subprocess.run(['systemd-analyze'], capture_output=True, text=True).stdout.split('\n')[0]
        units = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=active'], 
                               capture_output=True, text=True).stdout
        service_count = len([line for line in units.splitlines() if ".service" in line])
        return {"boot_summary": analyze.strip(), "active_services": service_count}
    except: return None