#!/usr/bin/env python3
"""
voice_indic.py - script.md ki Voice + Delivery lines se Kaif ki clone awaaz, IndicF5 (AI4Bharat, Hindi) se.

12 Nov 2026 se Chatterbox ki jagah. Chatterbox Hindi shabd galat bolta tha ("बंद" -> "बन", "तंदूर" -> "तंदूल").
IndicF5 Hindi ke liye bana hai. Sirf Kaif ki apni awaaz ka reference, kisi aur ki kabhi nahi.

Setup (ek baar): SETUP.md -> "Voice clone (IndicF5)". Venv `.venv-indic` (git mein nahi). Hugging Face par
ai4bharat/IndicF5 ki terms accept + `hf auth login` (Kaif khud karta hai, token chat mein nahi).

Usage (project root se):
    .venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md              # 2 take har line, best khud chunta hai
    .venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --takes 3
    .venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --use 3=2,5=1  # take khud chuno
    .venv-indic/bin/python tools/voice_indic.py episodes/epNNN/script.md --only 4 --seed 7   # ek line dobara
    .venv-indic/bin/python tools/voice_indic.py --line "फ़ोन है, कुल्फ़ी नहीं।" --josh 2

Emotion (josh): IndicF5 mein josh ka knob nahi hai. Reference jaisa andaaz, waisa clone. Isliye har josh ki alag
reference: brand/refs/josh5|josh4|josh3|josh2|sawaal (.wav/.m4a/.mp3) + same naam ki .txt (jo bola, shabd-ba-shabd).
Kaise record karna hai: brand/refs/RECORD.md. Jo file nahi hai, uski jagah brand/voice_ref.wav + brand/voice_ref.txt.
Josh 1-2 -> josh2, 3 -> josh3, 4 -> josh4, 5 -> josh5, aakhri scene (comment sawaal) -> sawaal.

Pace: model ki apni speed (tez 1.12 / normal 1.05 / dheema 0.95, x --speed), phir zaroorat ho to halka atempo
(max x1.12; Chatterbox mein x1.35 tha, usi se awaaz "phone call" jaisi dabti thi).

Best take: har take Whisper (medium) se suna jaata hai, jo script se sabse zyada milta hai woh chuna jaata hai.
Score episodes/epNNN/voice_takes_indic/_scores.json mein, aur 0.85 se kam par DHYAN.

Pronunciation: model wahi bolta hai jo likha hai. Galat bole to shabd ko bolchaal jaisa likho (SPOKEN list neeche,
ya script mein hi). Jaise "ऐप्स" ko "आप" bolta tha, isliye "एप्स".

Output:
    episodes/epNNN/voice_takes_indic/sNN_tK.wav   takes
    episodes/epNNN/voice.mp3                      chune hue takes, khamoshi kati, polish
    episodes/epNNN/voice_parts.json               har scene ki lambai (sec), edit timing ke liye
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from voice_clone import parse_script, take_af, wav_seconds, TARGET_WPM  # noqa: E402

SR = 24000
MODEL_SPEED = {"tez": 1.12, "normal": 1.05, "dheema": 0.95}
TEMPO_MAX = 1.12
REF_DIR = ROOT / "brand" / "refs"
DEFAULT_REF = ROOT / "brand" / "voice_ref.wav"
# Bolchaal wali spelling (model ke liye). Whisper/test se mile shabd yahan jodo.
SPOKEN = {"ऐप्स": "एप्स", "ऐप्पल": "एप्पल", "ऐप": "एप"}
# brand/refs/RECORD.md ke text (agar .txt na ho)
REF_TEXT = {
    "josh5": "क्या?! सच में? ये तो बिल्कुल उल्टा निकला! मुझे भी यकीन नहीं हुआ, लेकिन यही सच है। अब ध्यान से सुनो!",
    "josh4": "सुनो, ये बात बहुत काम की है। ज़्यादातर लोग यहीं गलती करते हैं, और फ़ोन की बैटरी खराब कर देते हैं।",
    "josh3": "चलो अब आराम से समझते हैं कि अंदर असल में होता क्या है। बात बिल्कुल सीधी है।",
    "josh2": "सोते हुए बच्चे को बार बार उठाओगे, तो वो और रोएगा। फ़ोन भी बिल्कुल ऐसा ही है।",
    "sawaal": "इन पाँच में से तुम कितनी करते थे? कमेंट में नंबर ज़रूर लिखना।",
}


def spoken(text):
    for a, b in SPOKEN.items():
        text = re.sub(rf"(?<![ऀ-ॿ]){a}(?![ऀ-ॿ])", b, text)
    return text


# Whisper kabhi English shabd Roman mein likhta hai (sahi bolne par bhi). Score se pehle Devanagari.
HEARD_FIX = {"apps": "एप्स", "app": "एप", "eps": "एप्स", "phone": "फोन", "battery": "बैटरी", "video": "वीडियो",
             "internet": "इंटरनेट", "google": "गूगल", "incognito": "इनकॉग्निटो", "website": "वेबसाइट",
             "office": "ऑफिस", "school": "स्कूल", "comment": "कमेंट", "number": "नंबर", "signal": "सिग्नल",
             "tower": "टावर", "history": "हिस्ट्री", "cover": "कवर", "fridge": "फ्रिज", "charging": "चार्जिंग",
             "charge": "चार्ज", "apple": "एप्पल", "chrome": "क्रोम", "100": "सौ", "100%": "सौ प्रतिशत", "5": "पाँच"}


def fix_heard(t):
    return " ".join(HEARD_FIX.get(w.strip(".,?!").lower(), w) for w in t.split())


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if ch not in "़ँंः")
    t = unicodedata.normalize("NFC", t)
    return "".join(ch for ch in t if ch.isalnum() or unicodedata.category(ch).startswith("M"))


def to_wav(src, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", "15", "-ac", "1", "-ar", str(SR),
                    "-af", "highpass=f=70,loudnorm=I=-18:TP=-2", str(dst)], check=True)
    return dst


def load_refs(tmp):
    """{naam: (wav, text)}. 'default' hamesha."""
    refs = {}
    dtxt = DEFAULT_REF.with_suffix(".txt")
    if not DEFAULT_REF.exists() or not dtxt.exists():
        sys.exit(f"Default reference chahiye: {DEFAULT_REF} aur {dtxt} (jo bola, shabd-ba-shabd)")
    refs["default"] = (to_wav(DEFAULT_REF, Path(tmp) / "ref_default.wav"), dtxt.read_text(encoding="utf-8").strip())
    for name in REF_TEXT:
        src = next((REF_DIR / f"{name}{e}" for e in (".wav", ".m4a", ".mp3", ".aac") if (REF_DIR / f"{name}{e}").exists()), None)
        if not src:
            continue
        txt = REF_DIR / f"{name}.txt"
        text = txt.read_text(encoding="utf-8").strip() if txt.exists() else REF_TEXT[name]
        refs[name] = (to_wav(src, Path(tmp) / f"ref_{name}.wav"), text)
    return refs


def pick_ref(refs, ln, last):
    want = "sawaal" if last else {1: "josh2", 2: "josh2", 3: "josh3", 4: "josh4", 5: "josh5"}[ln["josh"]]
    return (want, refs[want]) if want in refs else ("default", refs["default"])


def file_seconds(path):
    """Poori wav ki lambai, aakhir ki ruk samet. Edit timing isi se, taaki scene voice.mp3 se mile."""
    import wave
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def load_model():
    try:
        import numpy as np  # noqa: F401
        import soundfile as sf
        import torch
        import torchaudio
        from transformers import AutoModel
    except ImportError:
        sys.exit("IndicF5 venv se chalao: .venv-indic/bin/python tools/voice_indic.py ... (SETUP.md -> Voice clone)")

    def _load(path, *a, **k):  # torchaudio ko torchcodec chahiye; soundfile se padho
        x, sr = sf.read(str(path), dtype="float32", always_2d=True)
        return torch.from_numpy(x.T.copy()), sr
    torchaudio.load = _load
    print("IndicF5 load ho raha hai (pehli baar ~1.5 GB download)...")
    model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
    if torch.backends.mps.is_available():
        model.to("mps")  # Mac GPU: ~2 guna tez
    print("device:", model.device)
    return torch, model


def synth(torch, model, text, ref, speed, seed):
    import numpy as np
    model.config.speed = speed
    torch.manual_seed(seed)
    a = np.asarray(model(text, ref_audio_path=str(ref[0]), ref_text=ref[1]))
    return a.astype("float32") / 32768.0 if a.dtype == np.int16 else a.astype("float32")


_WM = None


def heard(path):
    global _WM
    from faster_whisper import WhisperModel
    if _WM is None:
        _WM = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, _ = _WM.transcribe(str(path), language="hi", condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in segs)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", nargs="?")
    ap.add_argument("--takes", type=int, default=2)
    ap.add_argument("--use", default="", help="'3=2,5=1' (scene=take), warna Whisper wala best")
    ap.add_argument("--only", default="", help="sirf yeh scenes dobara: '2,4'")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--speed", type=float, default=1.0, help="poori awaaz ki raftaar ka guna")
    ap.add_argument("--max-ruk", type=float, default=0.18)
    ap.add_argument("--line")
    ap.add_argument("--josh", type=int, default=3, choices=range(1, 6))
    ap.add_argument("--pace", default="normal", choices=list(MODEL_SPEED))
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.line:
        lines = [{"scene": 1, "text": args.line, "pace": args.pace, "josh": args.josh, "ruk": 0.3}]
        folder = ROOT / "output"
    elif args.script:
        lines = parse_script(args.script)
        folder = Path(args.script).resolve().parent
        if not lines:
            sys.exit("Script mein '[Scene N | ...] Voice: ... | Delivery: ...' wali line nahi mili.")
    else:
        ap.print_help()
        sys.exit(1)
    use = {int(a): int(b) for a, b in (p.split("=") for p in args.use.split(",") if p)}
    only = {int(x) for x in args.only.split(",") if x}
    tdir = folder / "voice_takes_indic"
    tdir.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else folder / ("voice_test.mp3" if args.line else "voice.mp3")
    scores_p = tdir / "_scores.json"
    scores = json.loads(scores_p.read_text(encoding="utf-8")) if scores_p.exists() else {}
    last_scene = lines[-1]["scene"]
    problems = []

    with tempfile.TemporaryDirectory() as tmp:
        refs = load_refs(tmp)
        print("References:", ", ".join(refs))
        todo = [(ln, k) for ln in lines for k in range(1, args.takes + 1)
                if (not only or ln["scene"] in only)
                and (only or args.line or not (tdir / f"s{ln['scene']:02d}_t{k}.wav").exists())]
        if todo:
            import soundfile as sf
            torch, model = load_model()
            for ln, k in todo:
                n = ln["scene"]
                rname, ref = pick_ref(refs, ln, n == last_scene and not args.line)
                sp = MODEL_SPEED[ln["pace"]] * args.speed
                text = spoken(ln["text"])
                print(f"Scene {n} take {k}: josh {ln['josh']}, {ln['pace']} (speed {sp:.2f}), ref {rname}: {text[:40]}")
                a = synth(torch, model, text, ref, sp, 1000 * n + k + args.seed)
                p = tdir / f"s{n:02d}_t{k}.wav"
                sf.write(str(p), a, SR)
                h = heard(p)
                r = difflib.SequenceMatcher(None, norm(fix_heard(h)), norm(text)).ratio()
                scores[p.name] = {"score": round(r, 3), "heard": h, "ref": rname}
                print(f"   milan {r:.2f}: {h}")
                scores_p.write_text(json.dumps(scores, ensure_ascii=False, indent=1), encoding="utf-8")

        parts, info = [], {}
        for i, ln in enumerate(lines):
            n = ln["scene"]
            cands = sorted(tdir.glob(f"s{n:02d}_t*.wav"))
            if not cands:
                sys.exit(f"Scene {n} ka take nahi mila.")
            if n in use:
                wav = tdir / f"s{n:02d}_t{use[n]}.wav"
            else:
                wav = max(cands, key=lambda c: scores.get(c.name, {}).get("score", 0))
            sc = scores.get(wav.name, {}).get("score")
            if sc is not None and sc < 0.85:
                problems.append(f"Scene {n} ({wav.name}) milan {sc:.2f}: \"{scores[wav.name]['heard']}\". "
                                f"Naya take: --only {n} --seed 5, ya shabd SPOKEN mein bolchaal jaisa likho")
            wpm = len(ln["text"].split()) / max(wav_seconds(wav), 0.1) * 60
            tempo = round(min(max(TARGET_WPM[ln["pace"]] * args.speed / max(wpm, 1), 1.0), TEMPO_MAX), 3)
            p = Path(tmp) / f"part_{i:02d}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", take_af(tempo, ln["ruk"], True, args.max_ruk),
                            "-ar", "48000", "-ac", "1", str(p)], check=True)
            parts.append(p)
            info[str(n)] = round(file_seconds(p), 3)  # poori file, ruk samet (warna video aage bhaagta hai)
            print(f"Scene {n}: {wav.name} (milan {sc}), {wpm:.0f} wpm -> x{tempo}")
        lst = Path(tmp) / "list.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        joined = Path(tmp) / "joined.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                        str(joined)], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "polish_voice.py"), str(joined), str(out),
                        "--no-tighten", "--denoise", "-35"], check=True, stdout=subprocess.DEVNULL)
    if not args.line:
        (folder / "voice_parts.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    if not args.line:
        real = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                     str(out)], capture_output=True, text=True).stdout or 0)
        if abs(real - sum(info.values())) > 0.3:
            problems.append(f"voice.mp3 {real:.2f}s par scene ka jod {sum(info.values()):.2f}s: video aur awaaz match nahi honge")
    print(f"\nAwaaz: {out}  ({sum(info.values()):.1f}s)")
    for p in problems:
        print("DHYAN:", p)


if __name__ == "__main__":
    main()
