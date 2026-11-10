# PoENavi

[日本語](README.md) | [English](README.en.md)

A Windows play-support tool for Path of Exile 1 and Path of Exile 2.

At startup you choose between **PoENavi**, which supports campaign progression and levelling, and **Poetrieve**, which helps with item price checks and trade searches.

> [!IMPORTANT]
> This product is not affiliated with or endorsed by Grinding Gear Games in any way.

## PoENavi features

- Automatic detection of area changes, level-ups and Act progression in PoE1 / PoE2
- Campaign guides, map images and experience-efficiency hints
- RTA timer with automatic laps
- Compact "Mini Navi" overlay (PoE1 / PoE2)
- Mini Navi voice guidance with VOICEVOX (PoE2)
- Gem acquisition list generated from Path of Building (PoE1)
- Area notes and detachable helper panels
<img width="2314" height="1219" alt="poenavi2" src="https://github.com/user-attachments/assets/fa1232cb-707c-432d-b4cd-d08e8611ea9f" />

## Poetrieve features

- Parses items copied in game and searches them through the official Trade API (PoE1 / PoE2)
- Adjust modifiers, value ranges, item states and search presets on screen
- Price list, price trends and reference prices for related items
- Configurable search hotkeys, with an interactive mode and AUTO-HIDE
- Notes, image management and Cheat sheets
- Dedicated search results window for OBS streaming
- Map mod check (PoE1)
- Reads Expedition rewards and shows poe.ninja prices converted to Exalted Orbs (PoE2)
- Reads the Abyss desecrated modifier Unveil screen and shows each modifier's tier (PoE2)
<img width="2090" height="1319" alt="poetore2" src="https://github.com/user-attachments/assets/9f3f0da0-d9be-42e8-831b-9eaf921207fa" />

## Shared features

- Choose PoE1 / PoE2 and the PoENavi / Poetrieve startup mode
- Minimise to and restore from the system tray
- Automatic updates
- Japanese or English interface (see [First-time setup](#first-time-setup))

Detailed feature explanations and illustrated how-to guides are available in these articles (Japanese):

- [How to use PoENavi](https://note.com/buri8857/n/nd1e6a07b8a29)
- [How to use Poetrieve](https://note.com/buri8857/n/n8a5047edab08)

## Download

1. Download the latest `PoENavi.zip` from [Releases](../../releases)
2. Right-click the ZIP and extract it with Windows' built-in "Extract All"
3. Run `PoENavi.exe` from the extracted folder

No Python installation is needed. Settings and notes are stored in `%APPDATA%\PoENavi\`, so they carry over when you update the app.

> [!WARNING]
> The current release is not signed with a code-signing certificate. Because of the internal structure of PyInstaller apps and limited download history, SmartScreen warnings or false positives from some antivirus products may occur.
>
> If SmartScreen appears, confirm that the publisher and download source are this repository, then run it via "More info". If you are unsure, do not run it; start the app directly from the public source instead.

### Virus scanning of release files

Each release's `PoENavi.zip` is scanned on VirusTotal, and the scan result URL and SHA-256 are posted on the corresponding Release page.

VirusTotal is a third-party service that checks the same file with multiple security products, including Microsoft's, and shows their verdicts together.
<img width="2168" height="1119" alt="poenavi" src="https://github.com/user-attachments/assets/e272273b-1273-4a7e-b7a1-a1daa59e33de" />
A matching SHA-256 also confirms that the scanned file and the released file are identical.

VirusTotal results do not fully guarantee safety, but they are published as independent supporting evidence.

See [Releases](../../releases) for the latest results.

### Code signing

Free code signing provided by [SignPath.io](https://signpath.io/), certificate by [SignPath Foundation](https://signpath.org/).

PoENavi has applied to the SignPath Foundation open-source code signing program to sign future Windows releases. Until the review and setup are complete, current releases are unsigned.

## First-time setup

1. On first launch, choose 日本語 or English. Existing installations stay in Japanese; the language can be changed later in Settings and takes effect after restarting PoENavi.
2. Choose PoE1 or PoE2
3. Choose "PoENavi" or "Poetrieve"
4. If you use PoENavi, check the location of `Client.txt` in Settings
5. If you use PoENavi, enable the "Local" chat channel in PoE's chat settings

To use Poetrieve, copy an item's information in game and press the search hotkey. The PoE2 Expedition reward price check is disabled by default; enable it from the dedicated button at the top of Poetrieve and set the read area to match your setup.

`Client.txt` is usually in one of the following locations and is normally detected automatically.

```text
PoE1 Steam: C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt
PoE2 Steam: C:\Program Files (x86)\Steam\steamapps\common\Path of Exile 2\logs\Client.txt
```

## Supported environments and limitations

- Officially supported: Windows 10 / 11
- Games: Path of Exile 1 / Path of Exile 2
- Poetrieve: PoE1 / PoE2
- PoB import: PoE1 only
- VOICEVOX narration: PoE2 only (VOICEVOX itself must be running)
- Expedition reward price check: PoE2 Poetrieve on Windows 10 / 11 only
- Linux: unofficial support; some Windows-specific features are not guaranteed to work
- If PoE's local chat log is disabled, some automatic laps and guide switching cannot be detected

## Safety and external communications

PoENavi runs independently from the game, and its source code is publicly available in this repository.

### Information read locally

- PoE's `Client.txt`: used to detect areas, levels, and Act progression
- Item information copied by the user: used for trade searches in Poetrieve
- The PoE window position and process name: used to identify the target window
- Images of PoE2 screen regions selected by the user: used for local OCR of Expedition rewards and Abyss Desecration modifiers

Settings, notes, timer records, price caches, screenshots, and OCR processing remain on the user's PC. The contents of `Client.txt`, personal notes, captured images, and OCR text are not uploaded.

### What PoENavi does not do

- Read or modify game memory
- Inject code into the game process
- Modify the game client or game files
- Intercept or alter network packets
- Automate combat, movement, or item interaction
- Collect PoE account credentials or session information

### OCR-based screen reading

The PoE2 Expedition reward price checker and Abyss Desecration modifier Tier checker run only when the user presses the configured shortcut.

1. A user-configured region of the PoE screen is captured through the operating system's screen-capture API.
2. Text is recognized locally using Windows OCR.
   - For an Abyss Desecration modifier only, if Windows OCR has a stable body but is missing a number, the automatically downloaded high-accuracy OCR pack (NDLOCR-Lite) rechecks that row locally.
3. The result is shown in a separate PoENavi window.

These OCR features do not read game memory or files, inject code, or interact with the game process. OCR results are never used to click, press keys, select modifiers, or perform any other in-game action automatically.

Captured images and recognized text are not sent to an external server. Expedition reference prices are obtained from poe.ninja, while Abyss Desecration modifier Tiers are determined using data bundled with PoENavi.

PoENavi's OCR features are designed with the Path of Exile Developer Policy in mind: they are manually initiated, read-only, processed locally, and displayed in a separate application window. This statement does not mean that PoENavi has been individually reviewed, endorsed, or approved by Grinding Gear Games. Please refer to the current official policies:

- [Path of Exile Developer Policy](https://www.pathofexile.com/developer/docs/index#policy)
- [Path of Exile Terms of Use](https://www.pathofexile.com/legal/terms-of-use-and-privacy-policy)

### External connections

- GitHub Releases: checking for and downloading updates
- Official Path of Exile Trade API: submitting item names, modifiers, values, and other search conditions
- poe.ninja: obtaining reference prices for currencies and items
- Official Path of Exile CDN and related services: downloading item images

Some non-OCR features can send search text or chat commands to PoE, but only in response to an explicit user action. OCR results never initiate keyboard or mouse input to the game. When the logout feature is enabled and its shortcut is pressed, PoENavi disconnects the PoE client's TCP connection.

## Updates

At startup, PoENavi checks GitHub Releases for the latest stable version. Choosing "Update now" downloads the ZIP, verifies its SHA-256, updates the files and restarts PoENavi.

To check manually, use "App info → Check for updates" in Settings.

## Uninstalling

PoENavi does not use an installer or a Windows service. To uninstall it, close PoENavi and delete the extracted `PoENavi` folder.

To also delete settings, notes and timer records, delete `%APPDATA%\PoENavi\`. Back up anything you want to keep first.

## Bug reports and requests

Report issues on [GitHub Issues](../../issues) with the following information:

- PoENavi version
- PoE1 / PoE2, and whether you were using PoENavi or Poetrieve
- Steps to reproduce and the behaviour you expected
- Error messages or screenshots

Do not post personal information, PoE credentials, API keys or similar.

## Running from source

```bash
git clone <this repository's URL>
cd <repository folder>
pip install -r requirements.txt
python main.py
```

Run the tests with:

```bash
python -m pytest -q
```

For the localization architecture, translation maintenance and validation, see [Localization Development](docs/localization.md).

## Technology

- Python 3.12+
- PySide6 (Qt 6)
- pynput / Windows API
- urllib3
- miniaudio (playback of WAV / MP3 notification sounds)
- Windows OCR (PoE2 Expedition reward reading)
- NDLOCR-Lite 1.3.1 (fallback only when digits are missing from PoE2 Abyss desecrated modifiers)
- PyInstaller

## License, disclaimer and credits

- [MIT License](LICENSE)
- [Third-party licenses and data sources](THIRD_PARTY_NOTICES.md)
- [Privacy policy](PRIVACY.md)
- [Code signing policy](docs/CODE_SIGNING_POLICY.md)
- [Path of Exile](https://www.pathofexile.com/) by Grinding Gear Games
- Built with ❤️ by [Buri](https://github.com/buri34)

Path of Exile, in-game names, items and related game data are the property of Grinding Gear Games.

## Support

If you like PoENavi, support for maintaining and improving its development environment would be greatly appreciated.

- [OFUSE](https://ofuse.me/48eca107)
- [Ko-fi](https://ko-fi.com/buri8857)
- [Patreon](https://www.patreon.com/cw/Buri8857)
