#!/usr/bin/env python3
"""
voice_clone.py - script.md ki Voice + Delivery lines se Kaif ki apni (clone) awaaz banana.

Free, local, MIT licence model: Chatterbox Multilingual (Resemble AI), Hindi.
Sirf Kaif ki apni awaaz ka reference use karo. Kisi aur ki awaaz kabhi nahi.

Setup (ek baar): SETUP.md -> "Voice clone". Alag venv `.venv-voice` (git mein nahi).

Usage (project root se, voice venv ke python se):
    .venv-voice/bin/python tools/voice_clone.py episodes/ep001/script.md
    .venv-voice/bin/python tools/voice_clone.py episodes/ep001/script.md --takes 3
    .venv-voice/bin/python tools/voice_clone.py episodes/ep001/script.md --use 2=3,4=2
    .venv-voice/bin/python tools/voice_clone.py --line "ये कोई हैक नहीं है।" --josh 5 --pace tez
Windows: .venv-voice\\Scripts\\python tools\\voice_clone.py ...

Script line format (prompts/script-style-guide.md):
    [Scene 1 | 0-2s] Voice: <Devanagari> | Delivery: tez, josh 5, zor "शब्द", ruk 0.5 | Action: ... | Visual: ...

Delivery se kya padha jaata hai:
    tez / normal / dheema   -> pace. Har take naap ke 195 / 180 / 160 shabd/min tak tez hota hai (--speed se aur)
    josh 1-5                -> kitna josh (model ka exaggeration). Na likho to 3.
    ruk <sec>               -> line ke baad khamoshi. Na likho to 0.3. Khamoshi kat ke tight hoti hai:
                               aam ruk 0.18s tak, 0.4+ wala 0.28s tak, line ke andar ki lambi chup 0.1s (--no-tighten se band)
    zor "..."               -> sirf Kaif/recording ke liye; model ek shabd par zor control nahi karta.

Output:
    episodes/epNNN/voice_takes/sNN_tK.wav   har line ke takes
    episodes/epNNN/voice.mp3                jude hue chosen takes, polish ke saath
"""
import argparse
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

JOSH = {1: 0.3, 2: 0.45, 3: 0.6, 4: 0.75, 5: 0.9}          # exaggeration (1.0+ par model bakwaas tail bolta hai)
# (cfg_weight, purana atempo: sirf --no-auto-speed par). cfg 0.0: 11 Nov 2026 ke test mein reference se awaaz sabse zyada milti
# thi (speaker similarity 0.925 vs 0.907 cfg .5). cfg_weight reference ki raftaar/andaaz ko dabata nahi, isliye 0.0.
PACE = {"tez": (0.0, 1.06), "normal": (0.0, 1.0), "dheema": (0.0, 0.95)}
# Har take ko is raftaar (shabd/minute) tak tez kiya jaata hai. Clone apne aap ~150 wpm bolta hai,
# jo Shorts ke liye dheema hai. Pitch nahi badalti (atempo).
TARGET_WPM = {"tez": 195, "normal": 180, "dheema": 160}
TEMPO_MIN, TEMPO_MAX = 1.0, 1.35
MAX_CHARS = 250

LINE_RE = re.compile(r"\[Scene\s*(\d+)[^\]]*\]\s*(.*)", re.I)


def field(rest, name):
    m = re.search(name + r":\s*(.*?)\s*(?:\|\s*[A-Za-z]+:|$)", rest)
    return m.group(1).strip() if m else ""


def parse_delivery(text):
    t = text.lower()
    pace = next((p for p in ("dheema", "tez", "normal") if p in t), "normal")
    m = re.search(r"josh\s*([1-5])", t)
    josh = int(m.group(1)) if m else 3
    m = re.search(r"ruk\s*([\d.]+)", t)
    ruk = float(m.group(1)) if m else 0.3
    return {"pace": pace, "josh": josh, "ruk": min(ruk, 2.0)}


def parse_script(path):
    lines = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(raw.strip())
        if not m:
            continue
        scene, rest = int(m.group(1)), m.group(2)
        voice = field(rest, "Voice")
        if not voice:
            continue
        d = parse_delivery(field(rest, "Delivery"))
        lines.append({"scene": scene, "text": voice, **d})
    return lines


def split_long(text):
    if len(text) <= MAX_CHARS:
        return [text]
    parts = [p.strip() for p in re.split(r"(?<=[।.?!])\s+", text) if p.strip()]
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) + 1 > MAX_CHARS:
            out.append(cur)
            cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        out.append(cur)
    return out


def pick_device(torch):
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_model():
    try:
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    except ImportError:
        sys.exit("Chatterbox nahi mila. Voice venv se chalao: .venv-voice/bin/python tools/voice_clone.py ...\n"
                 "Setup: SETUP.md -> Voice clone")
    device = pick_device(torch)
    print(f"Model load ho raha hai ({device}). Pehli baar ~3 GB download hota hai...")
    if device == "mps":
        # Kuch checkpoints cuda par save hain; MPS par CPU map karke load
        orig = torch.load

        def cpu_load(*a, **k):
            k.setdefault("map_location", torch.device("cpu"))
            return orig(*a, **k)
        torch.load = cpu_load
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    return torch, model


def wav_seconds(path):
    """Bolne ki lambai: shuru aur aakhir ki khamoshi (-45 dB se neeche) chhod ke."""
    with wave.open(str(path), "rb") as w:
        n, sr = w.getnframes(), float(w.getframerate())
        raw = w.readframes(n)
    try:
        import numpy as np
        x = np.abs(np.frombuffer(raw, dtype="<i2").astype("float32")) / 32768.0
        loud = np.nonzero(x > 10 ** (-45 / 20))[0]
        if len(loud):
            return (loud[-1] - loud[0] + 1) / sr
    except ImportError:
        pass
    return n / sr


def auto_tempo(wav, text, pace, speed):
    """Take ki asli raftaar naap ke utna hi tez karo jitna target ke liye chahiye."""
    sec = max(wav_seconds(wav), 0.1)
    wpm = len(text.split()) / sec * 60.0
    tempo = TARGET_WPM[pace] * speed / max(wpm, 1.0)
    return round(min(max(tempo, TEMPO_MIN), TEMPO_MAX), 3), wpm


def eff_ruk(ruk, max_ruk):
    """Line ke baad ki khamoshi. Aam ruk max_ruk tak kat jaata hai (jump cut jaisa tight);
    script mein 0.4+ likha ho (hansi/reveal se pehle) to thoda zyada bachta hai."""
    if max_ruk <= 0:
        return ruk
    return min(ruk, max_ruk + 0.1) if ruk >= 0.4 else min(ruk, max_ruk)


def take_af(tempo, ruk, tighten=True, max_ruk=0.18):
    """Ek take ka ffmpeg filter: kinaron ki khamoshi hatao, line ke andar ki lambi khamoshi 0.1s karo,
    tez karo, phir ruk. voice_clone aur episode ki make_episode.py dono yahi use karte hain (timing same rahe)."""
    af = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB,areverse")
    if tighten:
        af += ",silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-40dB:stop_silence=0.1"
    if abs(tempo - 1.0) > 1e-3:
        af += f",atempo={tempo}"
    return af + f",apad=pad_dur={eff_ruk(ruk, max_ruk) if tighten else ruk}"


def write_wav(path, samples, sr):
    import numpy as np
    x = np.clip(samples, -1.0, 1.0)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def prep_ref(ref, start, tmp):
    out = Path(tmp) / "ref.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", "12", "-i", str(ref),
                    "-ac", "1", "-ar", "24000", "-af", "highpass=f=70,loudnorm=I=-18:TP=-2", str(out)],
                   check=True)
    return out


def max_seconds(text):
    """Hindi ~10 akshar/sec. Isse bahut lamba take = model line ke baad bhi bol raha hai."""
    return len(text) / 10.0 * 1.8 + 1.0


def synth_part(torch, model, part, ref, josh, cfg, seed, temperature):
    """Take banao; agar line ke hisaab se bahut lamba ho (bakwaas tail), naye seed aur
    thode kam josh se dobara. 4 koshish, phir sabse chhota rakho aur warning do."""
    limit = max_seconds(part)
    best = None
    for attempt in range(4):
        exag = max(0.3, JOSH[josh] - 0.15 * (attempt // 2))
        torch.manual_seed(seed + 97 * attempt)
        wav = model.generate(part, language_id="hi", audio_prompt_path=str(ref),
                             exaggeration=exag, cfg_weight=cfg, temperature=temperature)
        x = wav.squeeze(0).detach().cpu().numpy()
        sec = len(x) / model.sr
        if best is None or sec < best[1]:
            best = (x, sec)
        if sec <= limit:
            return x, None
        print(f"   take bahut lamba ({sec:.1f}s, limit {limit:.1f}s), dobara bana raha hoon...")
    return best[0], f"{best[1]:.1f}s lamba hai (limit {limit:.1f}s). Suno, extra shabd ho sakte hain."


def synth(torch, model, text, ref, josh, pace, seed, temperature):
    import numpy as np
    cfg, _ = PACE[pace]
    chunks, warns = [], []
    for part in split_long(text):
        x, warn = synth_part(torch, model, part, ref, josh, cfg, seed, temperature)
        if warn:
            warns.append(warn)
        chunks.append(x)
        chunks.append(np.zeros(int(model.sr * 0.12), dtype="float32"))
    audio = np.concatenate(chunks[:-1]) if chunks else np.zeros(1, dtype="float32")
    return audio, warns


def assemble(items, out_mp3, tmp):
    """items: list of (wav_path, ffmpeg filter). Jodo, phir polish_voice."""
    parts = []
    for i, (wav, af) in enumerate(items):
        p = Path(tmp) / f"part_{i:02d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", af,
                        "-ar", "48000", "-ac", "1", str(p)], check=True)
        parts.append(p)
    lst = Path(tmp) / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    joined = Path(tmp) / "joined.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(joined)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "polish_voice.py"), str(joined), str(out_mp3),
                    "--no-tighten", "--denoise", "-35"], check=True, stdout=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", nargs="?", help="episodes/epNNN/script.md")
    ap.add_argument("--ref", help="Kaif ki saaf, josh wali recording (default brand/voice_ref.wav, warna brand/voice.mp3 ka pehla hissa)")
    ap.add_argument("--ref-start", type=float, default=0.0, help="reference mein kis second se 12s lena hai")
    ap.add_argument("--takes", type=int, default=1, help="har line ke kitne alag take")
    ap.add_argument("--use", default="", help="kaunsa take jodna: '2=3,4=2' (scene=take). Baaki take 1")
    ap.add_argument("--only", default="", help="sirf yeh scenes dobara banao: '2,4'")
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--speed", type=float, default=1.0,
                    help="poori awaaz ki raftaar ka guna (1.0 = tez 195 / normal 180 / dheema 160 shabd/min). Aur tez: 1.1")
    ap.add_argument("--no-tighten", action="store_true", help="khamoshi mat kaato (script ka poora ruk rakho)")
    ap.add_argument("--max-ruk", type=float, default=0.18, help="line ke baad zyada se zyada kitni khamoshi (sec). 0.4+ wale ruk ko 0.1 zyada milta hai")
    ap.add_argument("--no-auto-speed", action="store_true", help="purana tareeka: har take ko naape bina fixed atempo")
    ap.add_argument("--out", help="default: script ke folder mein voice.mp3")
    ap.add_argument("--line", help="test: ek line bolo (script ki jagah)")
    ap.add_argument("--josh", type=int, default=3, choices=range(1, 6))
    ap.add_argument("--pace", default="normal", choices=list(PACE))
    args = ap.parse_args()

    if args.line:
        lines = [{"scene": 1, "text": args.line, "pace": args.pace, "josh": args.josh, "ruk": 0.3}]
        folder = ROOT / "output"
    elif args.script:
        lines = parse_script(args.script)
        folder = Path(args.script).resolve().parent
        if not lines:
            sys.exit("Script mein '[Scene N | ...] Voice: ... | Delivery: ...' wali koi line nahi mili.")
    else:
        ap.print_help()
        sys.exit(1)

    ref = Path(args.ref) if args.ref else (ROOT / "brand" / "voice_ref.wav")
    if not ref.exists():
        ref = ROOT / "brand" / "voice.mp3"
        print("Note: brand/voice_ref.wav nahi mila, brand/voice.mp3 use ho raha hai. "
              "Josh wali 10-15s recording brand/voice_ref.wav mein daalo, clone bhi utna josh lega.")
    if not ref.exists():
        sys.exit(f"Reference nahi mila: {ref}")

    use = {}
    for pair in filter(None, args.use.split(",")):
        s, t = pair.split("=")
        use[int(s)] = int(t)
    only = {int(x) for x in filter(None, args.only.split(","))}

    takes_dir = folder / "voice_takes"
    takes_dir.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else folder / ("voice_test.mp3" if args.line else "voice.mp3")

    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        ref_wav = prep_ref(ref, args.ref_start, tmp)
        need = [ln for ln in lines if not only or ln["scene"] in only]
        missing = [ln for ln in need for k in range(1, args.takes + 1)
                   if args.only or not (takes_dir / f"s{ln['scene']:02d}_t{k}.wav").exists()]
        if missing or args.line:
            torch, model = load_model()
            for ln in need:
                for k in range(1, args.takes + 1):
                    path = takes_dir / f"s{ln['scene']:02d}_t{k}.wav"
                    if path.exists() and not only and not args.line:
                        continue
                    print(f"Scene {ln['scene']} take {k}: josh {ln['josh']}, {ln['pace']}  {ln['text'][:40]}")
                    audio, warns = synth(torch, model, ln["text"], ref_wav, ln["josh"], ln["pace"],
                                         seed=1000 * ln["scene"] + k, temperature=args.temperature)
                    write_wav(path, audio, model.sr)
                    problems += [f"Scene {ln['scene']} take {k}: {w}" for w in warns]

        items = []
        for ln in lines:
            k = use.get(ln["scene"], 1)
            wav = takes_dir / f"s{ln['scene']:02d}_t{k}.wav"
            if not wav.exists():
                sys.exit(f"Take nahi mila: {wav}. --takes {k} ke saath chalao.")
            if args.no_auto_speed:
                tempo = PACE[ln["pace"]][1] * args.speed
            else:
                tempo, wpm = auto_tempo(wav, ln["text"], ln["pace"], args.speed)
                print(f"Scene {ln['scene']}: {wpm:.0f} wpm -> x{tempo} ({ln['pace']})")
                if wpm < 110:
                    problems.append(f"Scene {ln['scene']} take {k}: bahut dheema ({wpm:.0f} wpm). "
                                    f"Naya take lo: --only {ln['scene']} --takes 3")
            items.append((wav, take_af(tempo, ln["ruk"], not args.no_tighten, args.max_ruk)))
        assemble(items, out, tmp)

    print(f"\nTakes: {takes_dir}")
    print(f"Awaaz: {out}")
    for p in problems:
        print("DHYAN:", p)
    print("Suno. Koi line achhi na lage: --takes 3 se naye take, phir --use scene=take.")


if __name__ == "__main__":
    main()
