import json
import os
from datetime import datetime
from colorama import Fore, Style

BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

class BackupManager:
    def __init__(self, vod_file="data/vod.json", channels_file="data/channels.json"):
        self.vod_file = vod_file
        self.channels_file = channels_file

    def backup_data(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")

        data = {
            "channels": self.load_data(self.channels_file),
            "vod": self.load_data(self.vod_file)
        }

        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(Fore.GREEN + f"\n📦 Backup saved at {backup_file}" + Style.RESET_ALL)

    def restore_backup(self, backup_file):
        if os.path.exists(backup_file):
            with open(backup_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            with open(self.channels_file, "w", encoding="utf-8") as f:
                json.dump(data.get("channels", []), f, indent=4)

            with open(self.vod_file, "w", encoding="utf-8") as f:
                json.dump(data.get("vod", []), f, indent=4)

            print(Fore.GREEN + "\n✅ Backup restored successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Backup file not found!" + Style.RESET_ALL)

    def load_data(self, file):
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
