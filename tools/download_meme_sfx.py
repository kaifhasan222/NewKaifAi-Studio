#!/usr/bin/env python3
"""
Download meme sound effects (like 'faaah', 'vine boom', 'aayein') from Myinstants
into assets/sfx/, with automatic volume scaling (default 0.5 = 50% volume so earrape
meme clips don't overpower the voiceover).

Usage:
  # List India trending meme sounds:
  python3 tools/download_meme_sfx.py --india

  # Search meme sounds without downloading:
  python3 tools/download_meme_sfx.py "faah" --list

  # Download top match at 50% volume (default):
  python3 tools/download_meme_sfx.py "faaah"

  # Download specific result number (#2) with custom filename and 40% volume:
  python3 tools/download_meme_sfx.py "faah" --pick 2 --name faaah.mp3 --volume 0.4

  # Adjust volume of an already-downloaded local MP3 file to 50%:
  python3 tools/download_meme_sfx.py --file assets/sfx/faaah.mp3 --volume 0.5
"""

import argparse
import html
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

BASE_URL = "https://www.myinstants.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

CARD_RE = re.compile(
    r"play\('(/media/sounds/[^']+\.mp3)',\s*'[^']+',\s*'([^']+)'\)"
    r".*?<a[^>]*class=\"instant-link[^\"]*\"[^>]*>(.*?)</a>",
    re.S,
)
DIRECT_MP3_RE = re.compile(r"(/media/sounds/[^\"']+\.mp3)")


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_cards(page_html: str) -> list[dict]:
    seen = set()
    results = []
    for mp3_path, slug, raw_title in CARD_RE.findall(page_html):
        if mp3_path in seen:
            continue
        seen.add(mp3_path)
        title = html.unescape(re.sub(r"<[^>]+>", "", raw_title)).strip()
        results.append(
            {
                "title": title,
                "slug": slug,
                "mp3_path": mp3_path,
                "mp3_url": urllib.parse.urljoin(BASE_URL, mp3_path),
                "page_url": f"{BASE_URL}/en/instant/{slug}/",
            }
        )
    return results


def slugify_filename(name: str) -> str:
    name = name.strip().lower()
    if name.endswith(".mp3"):
        name = name[:-4]
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return f"{name or 'meme-sfx'}.mp3"


def scale_volume_ffmpeg(path: pathlib.Path, volume: float) -> bool:
    """Scale MP3 volume in-place using ffmpeg. Returns True if scaled."""
    if abs(volume - 1.0) < 1e-4:
        return False
    ffmpeg_bin = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if not pathlib.Path(ffmpeg_bin).exists() and not shutil.which("ffmpeg"):
        print("WARNING: ffmpeg not found, keeping original volume.", file=sys.stderr)
        return False

    with tempfile.NamedTemporaryFile(
        suffix=".mp3", dir=str(path.parent), delete=False
    ) as tmp:
        tmp_path = pathlib.Path(tmp.name)

    try:
        cmd = [
            ffmpeg_bin,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-af",
            f"volume={volume}",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(tmp_path),
        ]
        subprocess.run(cmd, check=True)
        tmp_path.replace(path)
        return True
    except Exception as exc:
        if tmp_path.exists():
            tmp_path.unlink()
        print(f"WARNING: volume scaling failed ({exc}), kept original.", file=sys.stderr)
        return False


def download_file(url: str, dest: pathlib.Path, volume: float = 0.5) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)
    scale_volume_ffmpeg(dest, volume)
    return dest.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search and download Indian/viral meme sound effects into assets/sfx/."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Sound name to search (e.g. 'faaah', 'vine boom') or direct Myinstants URL",
    )
    parser.add_argument(
        "--india",
        action="store_true",
        help="Browse/select from Myinstants India trending board (/en/index/in/)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only list matching sounds without downloading",
    )
    parser.add_argument(
        "--pick",
        type=int,
        default=1,
        help="Which result number to download (1-based, default: 1)",
    )
    parser.add_argument(
        "--name",
        help="Output filename inside --out-dir (e.g. faaah.mp3)",
    )
    parser.add_argument(
        "--out-dir",
        default="assets/sfx",
        help="Directory to save MP3 (default: assets/sfx)",
    )
    parser.add_argument(
        "--volume",
        type=float,
        default=0.5,
        help="Volume multiplier (default: 0.5 for 50%% volume; use 1.0 for original loud volume)",
    )
    parser.add_argument(
        "--file",
        help="Adjust volume of an existing local MP3 file instead of downloading",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Max results to display when listing (default: 15)",
    )
    args = parser.parse_args()

    # Case 0: Adjust volume of an existing local file
    if args.file:
        target = pathlib.Path(args.file)
        if not target.exists():
            print(f"ERROR: File not found: {target}", file=sys.stderr)
            return 1
        if scale_volume_ffmpeg(target, args.volume):
            print(
                f"Adjusted volume of {target} to {int(args.volume * 100)}% "
                f"({target.stat().st_size / 1024:.1f} KB)"
            )
        return 0

    if not args.query and not args.india:
        parser.print_help()
        return 1

    out_dir = pathlib.Path(args.out_dir)

    # Case 1: Direct URL or /media/sounds/ path
    if args.query and (
        args.query.startswith("http://")
        or args.query.startswith("https://")
        or args.query.startswith("/media/sounds/")
    ):
        q = args.query
        if q.endswith(".mp3") or "/media/sounds/" in q:
            mp3_url = urllib.parse.urljoin(BASE_URL, q)
            default_name = pathlib.Path(urllib.parse.urlparse(mp3_url).path).name
        else:
            page_html = fetch_html(q)
            m = DIRECT_MP3_RE.search(page_html)
            if not m:
                print(f"ERROR: No MP3 found on page: {q}", file=sys.stderr)
                return 1
            mp3_url = urllib.parse.urljoin(BASE_URL, m.group(1))
            default_name = pathlib.Path(m.group(1)).name

        filename = slugify_filename(args.name or default_name)
        dest = out_dir / filename
        size = download_file(mp3_url, dest, volume=args.volume)
        print(f"Downloaded: {dest} ({size / 1024:.1f} KB, volume: {int(args.volume * 100)}%)")
        print(f"Source URL: {mp3_url}")
        return 0

    # Case 2: India trending board or search query
    if args.india and not args.query:
        source_url = f"{BASE_URL}/en/index/in/"
    else:
        encoded = urllib.parse.quote_plus(args.query)
        source_url = f"{BASE_URL}/en/search/?name={encoded}"

    page_html = fetch_html(source_url)
    cards = parse_cards(page_html)

    if args.india and args.query:
        # Filter India trending first; fallback to search if not found
        q_low = args.query.lower()
        india_html = fetch_html(f"{BASE_URL}/en/index/in/")
        india_cards = [
            c
            for c in parse_cards(india_html)
            if q_low in c["title"].lower() or q_low in c["slug"].lower()
        ]
        if india_cards:
            cards = india_cards

    if not cards:
        print(f"No sounds found for '{args.query or 'India trending'}'.", file=sys.stderr)
        return 1

    # Always show top matches if --list or --india without --pick download
    if args.list or (args.india and not args.query and "--pick" not in sys.argv):
        header = (
            "India Trending Meme Sounds (Myinstants)"
            if args.india and not args.query
            else f"Search results for '{args.query}'"
        )
        print(f"=== {header} ===")
        for idx, c in enumerate(cards[: args.limit], 1):
            print(f"{idx:2d}. {c['title']:36s} -> {c['mp3_path']}")
        cmd_hint = (
            "python3 tools/download_meme_sfx.py --india --pick <num>"
            if args.india and not args.query
            else f'python3 tools/download_meme_sfx.py "{args.query}" --pick <num>'
        )
        print(f"\nDownload karne ke liye: {cmd_hint}")
        return 0

    idx = args.pick - 1
    if idx < 0 or idx >= len(cards):
        print(
            f"ERROR: --pick {args.pick} out of range (1..{len(cards)}).",
            file=sys.stderr,
        )
        return 1

    chosen = cards[idx]
    filename = slugify_filename(args.name or chosen["title"])
    dest = out_dir / filename
    size = download_file(chosen["mp3_url"], dest, volume=args.volume)
    print(f"Downloaded [{args.pick}]: {chosen['title']}")
    print(f"Saved to  : {dest} ({size / 1024:.1f} KB, volume: {int(args.volume * 100)}%)")
    print(f"Source    : {chosen['page_url']} ({chosen['mp3_url']})")
    print(
        "Note      : Meme soundboard clip (Myinstants). Use short cuts; "
        "record in assets/LICENSES.md."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
