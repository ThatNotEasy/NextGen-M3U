# NextGen-M3U 🎵📺
- NextGen-M3U is a powerful and user-friendly M3U playlist generator designed for IPTV and streaming enthusiasts. With support for OTT M3U, TiviMate JSON, and XSPF formats, this tool makes it easy to create and manage playlists with DRM support, Widevine license integration, and structured group handling.

## ✨ Features
- ✅ Generate Multiple Playlist Formats (M3U, JSON, XSPF)
- ✅ DRM Support (Widevine, PlayReady, ClearKey)
- ✅ Automatic Widevine License Handling (for OTT M3U)
- ✅ TiviMate-Compatible JSON Output
- ✅ Custom Channel Grouping & Metadata
- ✅ Colorful and Interactive CLI Interface

## 🔧 Installation
```
git clone https://github.com/ThatNotEasy/NextGen-M3U
cd NextGen-M3U
pip install -r requirements.txt
python main.py
```

## 📌 Usage
- 1️⃣ Select your desired playlist format
- 2️⃣ Add channels with name, group, URL, thumbnail, and DRM type
- 3️⃣ If Widevine is selected, enter a license key
- 4️⃣ Save and enjoy your custom IPTV playlist!

## 📂 Output Formats
- 📜 OTT M3U

```
#EXTM3U
#KODIPROP:inputstreamaddon=inputstream.adaptive
#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key=12d9a54e458d31975632be17a8dac010:aa6173e8795c9b0b2733df838934817f
#EXTINF:-1 tvg-id="1" tvg-name="My Channel" group-title="Sports",My Channel
https://example.com/stream.m3u8
```
- 📂 TiviMate JSON

```
{
    "playlists": [
        {
            "name": "My IPTV Playlist",
            "groups": ["Sports", "News"],
            "channels": [
                {
                    "id": "1",
                    "name": "My Channel",
                    "group": "Sports",
                    "url": "https://example.com/stream.m3u8",
                    "thumbnail": "https://example.com/logo.png",
                    "drm": "Widevine"
                }
            ]
        }
    ]
}
```
