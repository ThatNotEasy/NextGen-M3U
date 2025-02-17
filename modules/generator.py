import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from colorama import Fore, Style

# Ensure 'playlist' directory exists
os.makedirs("playlist", exist_ok=True)

def generate_m3u(channels):
    """Generate M3U Playlist with Widevine DRM support."""
    m3u_content = "#EXTM3U\n"
    for ch in channels:
        drm_props = ""
        if ch['drm'] == "Widevine" and ch.get('license_key'):
            drm_props = (
                f"#KODIPROP:inputstreamaddon=inputstream.adaptive\n"
                f"#KODIPROP:inputstream.adaptive.license_type=clearkey\n"
                f"#KODIPROP:inputstream.adaptive.license_key={ch['license_key']}\n"
            )
        m3u_content += (
            f"{drm_props}"
            f"#EXTINF:-1 tvg-id=\"{ch['id']}\" tvg-name=\"{ch['name']}\" group-title=\"{ch['group']}\",{ch['name']}\n"
            f"{ch['url']}\n"
        )
    return m3u_content

def generate_tivimate_json(channels):
    """Generate TiviMate JSON Playlist."""
    tivimate_structure = {
        "playlists": [
            {
                "name": "My IPTV Playlist",
                "groups": sorted({ch['group'] for ch in channels}),
                "channels": channels
            }
        ]
    }
    return json.dumps(tivimate_structure, indent=4)

def generate_xspf(channels):
    """Generate XSPF Playlist."""
    playlist = Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
    tracklist = SubElement(playlist, "trackList")
    
    for ch in channels:
        track = SubElement(tracklist, "track")
        SubElement(track, "title").text = ch['name']
        SubElement(track, "location").text = ch['url']
        SubElement(track, "annotation").text = ch['group']
        SubElement(track, "image").text = ch['thumbnail']
    
    return tostring(playlist, encoding='utf-8', method='xml').decode('utf-8')

def save_playlist(option, channels):
    """Save playlist based on user selection."""
    playlist_types = {
        "1": ("playlist.m3u", generate_m3u(channels)),
        "2": ("playlist_tivimate.json", generate_tivimate_json(channels)),
        "3": ("playlist.xspf", generate_xspf(channels))
    }
    
    filename, content = playlist_types.get(option, (None, None))
    
    if filename:
        filepath = os.path.join("playlist", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(Fore.GREEN + f"\n✅ Playlist saved as {filepath}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Invalid option! Could not save playlist." + Style.RESET_ALL)
