import sys
from colorama import init, Fore, Style
from modules.banners import clear_terminal, banners
from modules.generator import PlaylistGenerator
from modules.channels import add_channel, generate_channels_playlist
from modules.vod import add_vod, generate_vod_playlist

init(autoreset=True)

def main():
    generator = PlaylistGenerator()

    while True:
        clear_terminal()
        banners()
        
        print(Fore.GREEN + "\n⚠️  FOOTPRINTS NOTICE ⚠️" + Fore.RESET)
        print(Fore.RED + "═" * 50 + Fore.RESET)
        print(Fore.WHITE + "Before generating multiple playlists, you must manually input all data using the single generator options (1 & 2)." + Fore.RESET)
        print(Fore.WHITE + "Once you have added all the required channels and VOD, use options 3 & 4 to generate the playlists." + Fore.RESET)
        
        print("\n" + Fore.CYAN + "📌 MAIN MENU")
        print(Fore.RED + "═" * 50 + Style.RESET_ALL)
        print(Fore.GREEN + "  1️⃣  Add Live TV Channel        " + Fore.YELLOW + "(Single Playlist Generator)" + Fore.RESET)
        print(Fore.GREEN + "  2️⃣  Add Video On Demand (VOD)  " + Fore.YELLOW + "(Single Playlist Generator)\n" + Fore.RESET)
        print(Fore.GREEN   + "  3️⃣  Generate Multiple Channel Playlist" + Fore.RESET)
        print(Fore.GREEN   + "  4️⃣  Generate Multiple VOD Playlist" + Fore.RESET)
        print(Fore.RED    + "  5️⃣  Exit"  + Fore.RESET)
        print(Fore.MAGENTA + "═" * 50  + Fore.RESET)

        choice = input("\n👉 Enter choice (1-5): ").strip()

        if choice == "1":
            clear_terminal()
            banners()
            add_channel()
        elif choice == "2":
            clear_terminal()
            banners()
            add_vod()
        elif choice == "3":
            clear_terminal()
            banners()
            generate_channels_playlist(multiple=True)
        elif choice == "4":
            clear_terminal()
            banners()
            generate_vod_playlist(multiple=True)
        elif choice == "5":
            clear_terminal()
            banners()
            print(Fore.RED + "\n👋 Exiting... See you next time!\n" + Style.RESET_ALL)
            sys.exit()
        else:
            print(Fore.RED + "\n❌ Invalid choice! Please select a valid option." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
