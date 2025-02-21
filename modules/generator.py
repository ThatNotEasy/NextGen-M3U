import json
import os
import time
from datetime import datetime
from colorama import Fore, Style

# Define output directories
OUTPUT_DIR = "output"
PLAYLIST_DIR = os.path.join(OUTPUT_DIR, "playlist")
GENERATOR_DIR = os.path.join(OUTPUT_DIR, "generator")

# Ensure directories exist
os.makedirs(PLAYLIST_DIR, exist_ok=True)
os.makedirs(GENERATOR_DIR, exist_ok=True)

class PlaylistGenerator:
    def __init__(self):
        self.vod_file = os.path.join(GENERATOR_DIR, "vod.json")
        self.channels_file = os.path.join(GENERATOR_DIR, "channels.json")

    def generate_filename(self, base_name, extension):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"

    def load_data(self, file):
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_json(self, data, filename):
        file_path = os.path.join(GENERATOR_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(Fore.GREEN + f"\n✅ JSON data saved as {file_path}" + Style.RESET_ALL)

    def format_drm(self, item):
        if item["drmType"] != "none" and item.get("contentKeys"):
            drm_props = f"#KODIPROP:inputstream.adaptive.license_type={item['drmType'].lower()}\n"
            drm_props += f"#KODIPROP:inputstream.adaptive.license_key={json.dumps(item['contentKeys'])}\n" if isinstance(item['contentKeys'], dict) else f"#KODIPROP:inputstream.adaptive.license_key={item['contentKeys']}\n"
            return drm_props
        return ""

    def format_custom_headers(self, item):
        headers = ""
        if item.get("customHeaders"):
            for key, value in item["customHeaders"].items():
                headers += f'#EXTHTTP:{{"{key}":"{value}"}}\n'
        return headers

    def save_m3u_playlist(self, data, base_filename, is_vod=False):
        filename = self.generate_filename(base_filename, "m3u")
        file_path = os.path.join(PLAYLIST_DIR, filename)

        m3u_content = "#EXTM3U\n"
        for item in data:
            drm_props = self.format_drm(item)
            custom_headers = self.format_custom_headers(item)

            m3u_content += (
                f"\n#EXTINF:-1 tvg-name=\"{item['channelName' if not is_vod else 'vodTitle']}\" "
                f"tvg-logo=\"{item['thumbnailUrl']}\" group-title=\"{item['groupName' if not is_vod else 'vodTitle']}\","
                f"{item['channelName' if not is_vod else 'vodTitle']}\n"
                f"{custom_headers}{drm_props}{item['manifestUrl']}\n"
            )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(Fore.GREEN + f"\n✅ M3U Playlist saved as {file_path}" + Style.RESET_ALL)

    def generate_vod_playlist(self, multiple=False):
        vod_data = self.load_data(self.vod_file)
        base_filename = "vod_multiple_playlist" if multiple else "vod_playlist"
        self.save_m3u_playlist(vod_data, base_filename, is_vod=True)

    def generate_channels_playlist(self, multiple=False):
        channels_data = self.load_data(self.channels_file)
        base_filename = "channels_multiple_playlist" if multiple else "channels_playlist"
        self.save_m3u_playlist(channels_data, base_filename, is_vod=False)
