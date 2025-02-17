import os
import sys
from colorama import init, Fore, Style
from modules.banners import clear_terminal, banners
from modules.generator import save_playlist

init(autoreset=True)

def print_banner():
    """ Display colorful banner """
    print(Fore.CYAN + Style.BRIGHT + "🎵 Playlist Generator 🎵")
    print(Fore.MAGENTA + "=" * 40 + Style.RESET_ALL)

def get_input(prompt, options=None):
    """ Get user input with optional validation """
    while True:
        user_input = input(Fore.YELLOW + prompt + " " + Style.RESET_ALL).strip().lower()
        if options and user_input not in options:
            print(Fore.RED + "❌ Invalid choice! Please enter one of: " + ", ".join(options) + Style.RESET_ALL)
        else:
            return user_input

def select_drm():
    """ Prompt user for DRM selection, returns DRM type or 'none'. """
    drm_choice = get_input("🔒 Is this a DRM protected stream? (yes/no):", ["yes", "no"])
    if drm_choice == "yes":
        print(Fore.CYAN + "\nSelect DRM type:")
        print(Fore.YELLOW + "1️⃣  Widevine")
        print(Fore.YELLOW + "2️⃣  PlayReady")
        print(Fore.YELLOW + "3️⃣  ClearKey" + Style.RESET_ALL)

        drm_mapping = {"1": "Widevine", "2": "PlayReady", "3": "ClearKey"}
        drm_type = get_input("👉 Enter DRM type (1/2/3):", drm_mapping.keys())

        if drm_type == "1":  # If Widevine, prompt for license key
            license_key = input(Fore.BLUE + "🔑 Enter Widevine License Key (format: keyid:key): " + Style.RESET_ALL).strip()
            return "Widevine", license_key
        
        return drm_mapping[drm_type], None
    
    return "none", None

def add_channel(channels):
    """ Collects channel information and appends to channels list. """
    clear_terminal()
    print_banner()
    print(Fore.GREEN + "➕ Adding a New Channel\n" + Style.RESET_ALL)

    name = input(Fore.BLUE + "📺 Enter channel name: " + Style.RESET_ALL).strip()
    group = input(Fore.BLUE + "🗂  Enter channel group: " + Style.RESET_ALL).strip()
    url = input(Fore.BLUE + "🔗 Enter manifest URL: " + Style.RESET_ALL).strip()
    thumbnail = input(Fore.BLUE + "🖼  Enter thumbnail URL: " + Style.RESET_ALL).strip()
    drm_type, license_key = select_drm()

    channels.append({
        "id": str(len(channels) + 1),
        "name": name,
        "group": group,
        "url": url,
        "thumbnail": thumbnail,
        "drm": drm_type,
        "license_key": license_key  # Store license key if Widevine is selected
    })

    print(Fore.GREEN + "\n✅ Channel added successfully!" + Style.RESET_ALL)

def display_channels(channels):
    """ Displays all added channels. """
    if not channels:
        print(Fore.RED + "\n🚫 No channels added yet.\n" + Style.RESET_ALL)
        return

    print(Fore.CYAN + "\n--- 📜 Current Channel List ---\n" + Style.RESET_ALL)
    for idx, ch in enumerate(channels, start=1):
        drm_color = Fore.YELLOW if ch['drm'] != "none" else Fore.GREEN
        license_info = f"🔑 {ch['license_key']}" if ch['drm'] == "Widevine" and ch.get("license_key") else ""
        print(f"{Fore.BLUE}{idx}. {ch['name']} {Fore.WHITE}({ch['group']}) - {drm_color}DRM: {ch['drm']} {license_info}" + Style.RESET_ALL)
    print("\n")

def main():
    channels = []

    while True:
        clear_terminal()
        banners()
        print(Fore.CYAN + "📌 Select Playlist Format:")
        print(Fore.YELLOW + "1️⃣  OTT M3U Playlist")
        print(Fore.YELLOW + "2️⃣  TiviMate Playlist")
        print(Fore.YELLOW + "3️⃣  XSPF Playlist")
        print(Fore.RED + "4️⃣  Exit\n" + Style.RESET_ALL)

        choice = get_input("👉 Enter your choice (1-4):", ["1", "2", "3", "4"])
        if choice == "4":
            print(Fore.RED + "👋 Exiting... See you next time!\n" + Style.RESET_ALL)
            sys.exit()

        while True:
            clear_terminal()
            banners()
            display_channels(channels)
            print(Fore.GREEN + "🛠 Options:")
            print(Fore.YELLOW + "1️⃣  Add New Channel")
            print(Fore.CYAN + "2️⃣  Save Playlist & Return")
            print(Fore.RED + "3️⃣  Cancel & Return\n" + Style.RESET_ALL)

            option = get_input("👉 Select an option (1/2/3):", ["1", "2", "3"])
            if option == "1":
                add_channel(channels)
            elif option == "2":
                save_playlist(choice, channels)
                break
            else:
                print(Fore.RED + "\n🔙 Returning to main menu...\n" + Style.RESET_ALL)
                break

        input(Fore.YELLOW + "\n🔄 Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
