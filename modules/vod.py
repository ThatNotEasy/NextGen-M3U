import json
import os
from colorama import Fore, Style
from modules.generator import PlaylistGenerator

VOD_FILE = "output/generator/vod.json"
generator = PlaylistGenerator()

def load_vod():
    if os.path.exists(VOD_FILE):
        with open(VOD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_vod(vod_list):
    with open(VOD_FILE, "w", encoding="utf-8") as f:
        json.dump(vod_list, f, indent=4)

def get_license_key():
    print(Fore.YELLOW + "\n🔑 DRM Key Format:" + Style.RESET_ALL)
    print("   ⚡ Single Key: key_id:key_value (e.g., `123123:23414124`)")
    print("   🔷 Multiple Keys: JSON format (e.g., `{\"12123123\":\"123123123\", \"123123123\":\"234535353\"}`)\n")

    license_input = input(Fore.BLUE + "📝 Enter DRM Key: " + Style.RESET_ALL).strip()

    try:
        if license_input.startswith("{") and license_input.endswith("}"):
            return json.loads(license_input)
        elif ":" in license_input:
            key_id, key_value = license_input.split(":")
            return {key_id: key_value}
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + "\n❌ Invalid DRM key format. Please try again!\n" + Style.RESET_ALL)
        return get_license_key()

def get_custom_headers():
    custom_headers = {}
    add_headers = input(Fore.YELLOW + "\n⚙️  Add Custom Headers? (y/n): " + Style.RESET_ALL).strip().lower()

    if add_headers == "y":
        user_agent = input(Fore.BLUE + "🌐 Enter User-Agent: " + Style.RESET_ALL).strip()
        custom_headers["User-Agent"] = user_agent

        while True:
            key = input(Fore.BLUE + "🔑 Enter Header Key (or press Enter to finish): " + Style.RESET_ALL).strip()
            if not key:
                break
            value = input(Fore.BLUE + f"💡 Enter Value for `{key}`: " + Style.RESET_ALL).strip()
            custom_headers[key] = value

    return custom_headers if custom_headers else None

def add_vod():
    while True:
        print("\n" + Fore.GREEN + "🎬 ➕ Adding a New VOD" + Style.RESET_ALL)
        title = input(Fore.BLUE + "🏷️  VOD Title: " + Style.RESET_ALL).strip()
        url = input(Fore.BLUE + "🔗  VOD URL: " + Style.RESET_ALL).strip()
        thumbnail = input(Fore.BLUE + "🖼️  Thumbnail URL: " + Style.RESET_ALL).strip()

        drm = input(Fore.YELLOW + "🔒 Is DRM Protected? (y/n): " + Style.RESET_ALL).strip().lower()
        drm_type = "none"
        content_keys = None

        if drm == "y":
            drm_type = input("⚡ Select DRM Type (Widevine/PlayReady/ClearKey): ").strip()
            content_keys = get_license_key()

        custom_headers = get_custom_headers()

        vod_list = load_vod()
        vod_list.append({
            "vodTitle": title,
            "manifestUrl": url,
            "thumbnailUrl": thumbnail,
            "drmType": drm_type,
            "contentKeys": content_keys,
            "customHeaders": custom_headers
        })

        save_vod(vod_list)
        print(Fore.GREEN + "\n✅ VOD Added Successfully!\n" + Style.RESET_ALL)

        # Ask if user wants to continue adding VODs
        cont = input(Fore.YELLOW + "➕ Do you want to add another VOD? (y/n): " + Style.RESET_ALL).strip().lower()
        if cont != "y":
            print(Fore.CYAN + "\n👋 Exiting VOD Addition.\n" + Style.RESET_ALL)
            break

def generate_vod_playlist(multiple=False):
    generator.generate_vod_playlist(multiple)
