import json, os
from src.parser import get_service_description

DATA_DIR = "data"
USER_SERVICES_FILE = os.path.join(DATA_DIR, "user_services.json")
DEFAULT_SERVICES_FILE = os.path.join(DATA_DIR, "default_services.json")

def load_knowledge_base():
    kb = {}
    for path in [DEFAULT_SERVICES_FILE, USER_SERVICES_FILE]:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    if data: kb.update(data)
            except: continue
    return kb

def add_custom_rule(name, risk, note):
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    rules = {}
    is_update = False
    if os.path.exists(USER_SERVICES_FILE):
        with open(USER_SERVICES_FILE, 'r') as f:
            try:
                rules = json.load(f)
                is_update = name in rules
            except: rules = {}

    rules[name] = {"risk": int(risk), "note": f"[USER] {note}"}
    with open(USER_SERVICES_FILE, 'w') as f:
        json.dump(rules, f, indent=4)
    return "updated" if is_update else "added"

def delete_custom_rule(name):
    if not os.path.exists(USER_SERVICES_FILE): return False
    with open(USER_SERVICES_FILE, 'r') as f:
        try: rules = json.load(f)
        except: return False
    if name in rules:
        rules.pop(name)
        with open(USER_SERVICES_FILE, 'w') as f:
            json.dump(rules, f, indent=4)
        return True
    return False

def process_blame_data(raw_data, target_level=None, less=False, greater=False, equal=False, exclude_list=None):
    kb = load_knowledge_base()
    processed = []
    exclude_list = exclude_list or []
    for line in raw_data:
        parts = line.split()
        if len(parts) < 2: continue
        time, name = parts[0], parts[1]
        if name in exclude_list: continue
        if name in kb:
            risk, note = kb[name]['risk'], kb[name]['note']
        else:
            risk, note = 3, get_service_description(name)
        keep = True
        if target_level is not None:
            if less: keep = risk < target_level
            elif greater: keep = risk > target_level
            else: keep = risk == target_level
        if keep:
            processed.append({"name": name, "time": time, "risk": risk, "note": note})
    return processed