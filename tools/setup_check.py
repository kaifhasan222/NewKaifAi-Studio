#!/usr/bin/env python3
"""Check that the tools needed for the pipeline are installed (Mac + Windows + Linux)."""
import platform
import shutil
import sys

system = platform.system()  # Darwin = Mac, Windows, Linux
INSTALL = {
    "ffmpeg": {
        "Darwin": "brew install ffmpeg",
        "Windows": "winget install Gyan.FFmpeg   (phir terminal band karke dobara kholo)",
        "Linux": "sudo apt install ffmpeg",
    },
    "node": {
        "Darwin": "brew install node",
        "Windows": "winget install OpenJS.NodeJS.LTS",
        "Linux": "sudo apt install nodejs npm",
    },
}


def check(name, required=True):
    path = shutil.which(name)
    tag = "OK      " if path else ("MISSING " if required else "optional")
    print(f"[{tag}] {name:8s} {path or ''}")
    if not path:
        print(f"           install: {INSTALL.get(name, {}).get(system, 'see SETUP.md')}")
    return bool(path)


print(f"System: {system}, Python {sys.version.split()[0]}")
ok = check("ffmpeg") & check("ffprobe")
check("node", required=False)
try:
    import faster_whisper  # noqa: F401
    print("[OK      ] faster-whisper (captions)")
except ImportError:
    print("[optional] faster-whisper missing -> pip install faster-whisper   (captions ke liye)")
print("\nAll required tools found." if ok else "\nPehle MISSING tools install karo (SETUP.md dekho).")
sys.exit(0 if ok else 1)
