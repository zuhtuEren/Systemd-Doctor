import argparse, sys, os
from src.parser import get_systemd_blame_data, get_system_summary
from src.engine import process_blame_data, add_custom_rule, delete_custom_rule
from src.ui import display_blame_table, interactive_selection_menu, display_history, display_system_dashboard, interactive_restore_menu
from src.actions import SNAPSHOT_DIR, restore_snapshot, disable_selected_services

def main():
    parser = argparse.ArgumentParser(description="Systemd-Doctor v1.6.2 Master")
    parser.add_argument("-b", "--blame", action="store_true")
    parser.add_argument("-d", "--disable", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-H", "--history", action="store_true")
    parser.add_argument("-S", "--summary", action="store_true")
    parser.add_argument("--restore", nargs="?", const="LATEST")
    parser.add_argument("--add-rule", nargs=3, metavar=('SERVICE', 'RISK', 'NOTE'))
    parser.add_argument("--del-rule", metavar='SERVICE')
    parser.add_argument("level", type=int, nargs="?")
    parser.add_argument("-l", "--less", action="store_true")
    parser.add_argument("-g", "--greater", action="store_true")
    parser.add_argument("-e", "--equal", action="store_true")
    parser.add_argument("-x", "--exclude", nargs="+")

    args = parser.parse_args()

    if args.add_rule:
        service, risk, note = args.add_rule
        status = add_custom_rule(service, risk, note)
        print(f"[OK] {'Updated' if status == 'updated' else 'Added'}: {service}")
        return

    if args.del_rule:
        if delete_custom_rule(args.del_rule): print(f"[OK] Deleted: {args.del_rule}")
        else: print(f"[ERROR] Rule for {args.del_rule} not found.")
        return

    if len(sys.argv) == 1 or args.summary:
        display_system_dashboard(get_system_summary())
        if len(sys.argv) == 1: return

    if args.history:
        snaps = []
        if os.path.exists(SNAPSHOT_DIR):
            snaps = sorted([os.path.join(SNAPSHOT_DIR, f) for f in os.listdir(SNAPSHOT_DIR) if f.startswith("snapshot_")], 
                           key=os.path.getmtime, reverse=True)
        display_history(snaps)
        return

    if args.restore:
        snaps = []
        if os.path.exists(SNAPSHOT_DIR):
            # ctime yerine mtime (modification time) kullanıldı, Linux için daha güvenilir.
            snaps = sorted([os.path.join(SNAPSHOT_DIR, f) for f in os.listdir(SNAPSHOT_DIR) if f.startswith("snapshot_")], 
                           key=os.path.getmtime, reverse=True)
        
        if args.restore == "LATEST":
            if not snaps:
                print("[ERROR] No snapshots available. Perform an optimization first.")
                return
            
            # Seçim menüsünü çağır
            selected = interactive_restore_menu(snaps)
            if selected:
                restore_snapshot(selected)
        else:
            # Belirtilen dosyayı yükle
            restore_snapshot(args.restore)
        return

    if args.blame or args.disable:
        data = process_blame_data(get_systemd_blame_data(), args.level, args.less, args.greater, args.equal, args.exclude)
        if args.blame and not args.disable: display_blame_table(data)
        elif args.disable:
            sel = interactive_selection_menu(data) if args.interactive else [s['name'] for s in data]
            if sel: disable_selected_services(sel, data)

if __name__ == "__main__": main()