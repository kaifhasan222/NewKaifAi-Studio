#!/usr/bin/env python3
"""
cut_silence.py - Flow @me clips ki khamoshi kaat ke jump cuts banana (lip-sync same).

Dikkat: Flow clip 8 sec ki hoti hai, Kaif aksar 4-5 sec bolta hai. Shuru, beech aur aakhir ki
khamoshi video mein reh jaati thi. polish_voice.py ki gap-cutting Flow awaaz par nahi chal sakti
(honth aur awaaz alag ho jaate). Yeh tool VIDEO hi kaat deta hai: har clip ki awaaz mein bolne
wale hisse dhoondh ke usi clip ke chhote tukde (start/duration) bana deta hai. Phir
flow_voice.py aur build_video.py unhi tukdon se chalte hain, to awaaz aur honth saath rehte hain.

Usage (project root se):
    python tools/cut_silence.py episodes/ep004/episode.json
    python tools/cut_silence.py episodes/ep004/episode.json --gap 0.25 --pad 0.07 --db -32
    python tools/cut_silence.py episodes/ep004/episode.json --whisper   # .venv (faster-whisper) se

--whisper: Flow clip mein halki room-tone/hum ho to silencedetect khamoshi nahi pakadta. Yeh flag
Whisper ke word timestamps se pehle shabd se aakhri shabd tak hi rakhta hai, aur shabdon ke beech
lamba gap bhi kaatta hai.

Pehli baar original "clips" ko "clips_src" mein save karta hai. Dobara chalao to "clips_src" se
hi kaatta hai (tune karna safe). Clip par "nocut": true ho to woh clip waise hi rehti hai.
Clip par "cuts": [[a, b], ...] (clip ke seconds) = yeh hissa bhi hatao, jaise doharaya shabd.
Full clip ke jump cut par zoom badalta hai (normal <-> "tight"), taaki cut jhatka na lage.
Split clip mein upar wala card ruk ke dobara shuru nahi hota (card.media_start aage badhta hai).

Kaif ki apni raw recording (camera/phone) ke liye 2 aur flag (dono --whisper khud chalu karte hain):
    --fillers   "आ", "उम", "हम्म", "aa", "umm" jaise atakne wale shabd, aur turant doharaya shabd
                ("ये ये ऐप" -> "ये ऐप") kaat do. Extra shabd: --filler-words "मतलब,basically".
    --takes     script.md (episode.json ke saath wala, ya --script) ki har Voice line se bola hua
                hissa milao. Ek line 2-3 baar boli (retake, galat shuruaat) to woh take rakho jo
                line se sabse zyada milta hai (poori line, kam filler); barabar ho to aakhri take.
                Baaki takes kaat do. Script se na milne wala hissa report mein "extra" dikhta hai,
                --drop-extra do to woh bhi kata jaata hai.
    --dry-run   kuch save nahi, sirf report. Har baar report episode folder mein cut_report.txt.
    --model     Whisper model. --fillers/--takes par default medium (small Hindi mein galat sunta hai).
Galat take chuna gaya to clip par "keep": [[a, b]] (clip ke seconds) do: us hisse ka koi shabd
kabhi nahi katega. Report dekh ke "cuts" / "keep" se theek karo, phir dobara chalao.

Phir: python tools/flow_voice.py <episode.json>, phir build_video.py.
"""
import argparse
import copy
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


def probe_dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def speech_regions(f, start, dur, db, min_sil):
    """[start, start+dur] ke andar bolne wale hisse (clip time mein)."""
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", f, "-vn",
         "-af", f"highpass=f=90,silencedetect=n={db}dB:d={min_sil}", "-f", "null", "-"],
        capture_output=True, text=True)
    sil, s0 = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            s0 = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and s0 is not None:
            sil.append((s0, float(m.group(1))))
            s0 = None
    if s0 is not None:
        sil.append((s0, dur))
    regs, cur = [], 0.0
    for a, b in sil:
        if a > cur:
            regs.append((cur, a))
        cur = max(cur, b)
    if cur < dur:
        regs.append((cur, dur))
    return [(start + a, start + b) for a, b in regs]


_WM = None
_WCACHE = {}


def transcribe(f, model="small"):
    """Poori file ke Whisper words [(a, b, text)]. faster-whisper na ho to None.
    Har bolne wala tukda (VAD) alag se transcribe hota hai: ek saath do to Whisper doharayi
    line (retake) ko chhod deta hai, aur retake pakadna hi to kaam hai."""
    global _WM
    try:
        from faster_whisper import WhisperModel, decode_audio
        from faster_whisper.vad import VadOptions, get_speech_timestamps
    except ImportError:
        return None
    if f in _WCACHE:
        return _WCACHE[f]
    if _WM is None:
        print(f"  Whisper {model} load ho raha hai...")
        _WM = WhisperModel(model, compute_type="int8")
    sr = 16000
    au = decode_audio(f, sampling_rate=sr)
    chunks = get_speech_timestamps(au, VadOptions(min_silence_duration_ms=350, speech_pad_ms=150))
    ws = []
    for ch in chunks:
        off = ch["start"] / sr
        segs, _ = _WM.transcribe(au[ch["start"]:ch["end"]], language="hi", word_timestamps=True,
                                 condition_on_previous_text=False)
        for sg in segs:
            for w in sg.words or []:
                t = w.word.strip()
                a, b = w.start + off, w.end + off
                # padding ki wajah se tukde thoda overlap karte hain: wahi shabd dobara na gino
                if t and not (ws and a < ws[-1][1] - 0.05 and norm(t) == norm(ws[-1][2])):
                    ws.append((a, b, t))
    _WCACHE[f] = ws
    return ws


def word_spans(f, start, dur, model="small"):
    """Whisper words [(a, b)] clip time mein. faster-whisper na ho to None."""
    ws = transcribe(f, model)
    if ws is None:
        return None
    return [(a, b) for a, b, _ in ws if b > start and a < start + dur]


# ---------- filler + best take ----------

FILLERS = {"आ", "आं", "आँ", "अ", "अं", "उम", "उम्म", "अम्म", "हम्म", "हम्मम", "ऊ", "ऊं", "उह",
           "एह", "ओह", "aa", "aaa", "ah", "um", "umm", "uh", "uhh", "hmm", "hm", "er", "erm", "eh"}


def norm(t):
    """Milane ke liye: chhote akshar, nukta/bindu/visarg hatao, sirf akshar-ank."""
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if ch not in "\u093c\u0901\u0902\u0903")
    t = unicodedata.normalize("NFC", t)
    return "".join(ch for ch in t if ch.isalnum() or unicodedata.category(ch).startswith("M"))


def is_filler(text, extra):
    n = norm(text)
    if not n:
        return False
    if n in {norm(x) for x in FILLERS | extra}:
        return True
    # "आआआ", "उम्मम", "aaaa": lambi kheenchi hui awaaz. "हम" (we), "ए" (ए आई) filler nahi
    return bool(re.fullmatch(r"(आ+|अ+|ऊ+|उ?म्म+|ह+म्म+|a{2,}h*|u+m+|u+h+|h+m{2,}|e+r+m*)", n))


def script_lines(path):
    """script.md ki Voice lines (Devanagari), scene order mein."""
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.search(r"Voice:\s*(.+?)\s*(\||$)", line)
        if m and norm(m.group(1)):
            sc = re.search(r"Scene\s*(\d+)", line)
            out.append({"scene": int(sc.group(1)) if sc else len(out) + 1, "text": m.group(1)})
    return out


def phrases(words, gap=0.45):
    """Words ko bolne ke tukdon mein todo (beech mein > gap chup = naya tukda)."""
    out, cur = [], []
    for w in words:
        if cur and w["a"] - cur[-1]["b"] > gap:
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def match(spoken, line):
    """(spoken ka kitna hissa line se hai, line ka kitna hissa bola gaya, line mein kahan tak)."""
    sm = difflib.SequenceMatcher(None, spoken, line, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 2]
    hit = sum(b.size for b in blocks)
    if not hit:
        return 0.0, 0.0, 0, 0
    return hit / max(1, len(spoken)), hit / max(1, len(line)), blocks[0].b, blocks[-1].b + blocks[-1].size


def pick_takes(words, lines, min_prec=0.5):
    """Har word par "take" (line idx, take no.) lagao. Return: {line: [takes]}, extras.
    take = {"words": [...], "cov": line ka kitna bola, "fill": filler count}."""
    takes, extras, last = {}, [], None
    for ph in phrases(words):
        sp = norm("".join(w["t"] for w in ph if not w["filler"]))
        if not sp:
            continue
        best = None
        for i, ln in enumerate(lines):
            prec, cov, lo, hi = match(sp, ln["n"])
            # thoda aage wali line ko pasand karo (order), par order zabardasti nahi
            score = prec + (0.03 if last is not None and i == last[0] + 1 else 0)
            if best is None or score > best[0]:
                best = (score, i, prec, lo, hi)
        if best is None or best[2] < min_prec:
            extras.append(ph)
            continue
        _, i, _, lo, hi = best
        tk = takes.setdefault(i, [])
        # pichhla tukda isi line ka tha aur yeh usi line mein aage ka hissa hai = same take (beech ka ruk)
        if last is not None and last[0] == i and tk and lo >= tk[-1]["hi"] - 3:
            tk[-1]["words"] += ph
            tk[-1]["hi"] = max(tk[-1]["hi"], hi)
        else:
            tk.append({"words": list(ph), "hi": hi})
        last = (i, len(tk) - 1)
    for i, tk in takes.items():
        for t in tk:
            sp = norm("".join(w["t"] for w in t["words"] if not w["filler"]))
            t["cov"] = match(sp, lines[i]["n"])[1]
            t["prec"] = match(sp, lines[i]["n"])[0]
            t["fill"] = sum(w["filler"] for w in t["words"])
            # poori line + script jaisi + kam atakna; 0.04 andar = barabar -> aakhri take jeete
            t["score"] = t["cov"] * 0.7 + t["prec"] * 0.3 - 0.03 * t["fill"]
        win = max(range(len(tk)), key=lambda k: (round(tk[k]["score"] / 0.04), k))
        for k, t in enumerate(tk):
            t["keep"] = k == win
    return takes, extras


# asli doharav, kaatna nahi
REDUP = {"बार बार", "धीरे धीरे", "जल्दी जल्दी", "अलग अलग", "कभी कभी", "साथ साथ", "बहुत बहुत", "थोड़ा थोड़ा",
         "रोज़ रोज़", "एक एक", "दो दो", "हाँ हाँ", "नहीं नहीं", "चलो चलो", "very very", "bye bye"}


def stutters(words, allowed=""):
    """Atakna aur galat shuruaat: "ये ये ऐप" -> pehla "ये"; "एक स्कैन और कुछ से | एक स्कैन और कुछ
    सेकंड" -> pehli adhoori koshish. Shabd i se shuru hua hissa 12 shabd ke andar dobara shuru ho
    (kam se kam aadha milke) to pehli copy kaato. Jo doharav script/REDUP mein hai woh nahi."""
    ns = [norm(w["t"]) for w in words]
    ok = {norm(x) for x in REDUP}
    al = norm(allowed)
    drop, i = set(), 0
    while i < len(words):
        hit = None
        for j in range(i + 1, min(len(words), i + 13)):
            if words[j]["a"] - words[j - 1]["b"] > 1.5:
                break
            k = 0
            while j + k < len(words) and i + k < j and ns[i + k] and ns[i + k] == ns[j + k]:
                k += 1
            if k and (k >= 2 or j == i + 1) and k * 2 >= min(j - i, 4):
                pair = "".join(ns[i:j + k])
                if pair in ok or (al and pair in al):
                    break
                hit = j
                break
        if hit:
            drop.update(range(i, hit))
            i = hit
        else:
            i += 1
    return drop


def hole(words, idxs):
    """Lagaatar words idxs ka kaatne wala hissa, padosi shabdon ko chhue bina."""
    i0, i1 = min(idxs), max(idxs)
    a = words[i0]["a"] - 0.04
    b = words[i1]["b"] + 0.04
    if i0 > 0:
        a = max(a, words[i0 - 1]["b"] + 0.02)
    if i1 + 1 < len(words):
        b = min(b, words[i1 + 1]["a"] - 0.02)
    return (a, b)


def runs(idxs):
    """Indices ko lagaatar tukdon mein."""
    out = []
    for i in sorted(idxs):
        if out and i == out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return out


def fmt(ws):
    return " ".join(w["t"] for w in ws)


def plan_cuts(src, args, script):
    """Har clip (index) ke liye extra holes, aur report lines."""
    extra = {x.strip() for x in (args.filler_words or "").split(",") if x.strip()}
    words = []  # saari clips ke words, order mein
    for ci, c in enumerate(src):
        if c.get("nocut"):
            continue
        f = c["file"]
        start = float(c.get("start") or 0)
        dur = float(c.get("duration") or 0) or probe_dur(f) - start
        ws = transcribe(f, args.model)
        if ws is None:
            sys.exit("--fillers/--takes ke liye faster-whisper chahiye (.venv/bin/python se chalao)")
        keep = c.get("keep", [])
        for a, b, t in ws:
            if b > start and a < start + dur:
                words.append({"ci": ci, "a": a, "b": b, "t": t, "filler": is_filler(t, extra),
                              "lock": any(k0 <= (a + b) / 2 <= k1 for k0, k1 in keep)})
    drop, why, rep = set(), {}, []
    if args.fillers:
        for i, w in enumerate(words):
            if w["filler"] and not w["lock"]:
                drop.add(i)
                why[i] = "filler"
        for ci in {w["ci"] for w in words}:
            idx = [i for i, w in enumerate(words) if w["ci"] == ci and i not in drop]
            for k in stutters([words[i] for i in idx], " ".join(ln["text"] for ln in script or [])):
                if not words[idx[k]]["lock"]:
                    drop.add(idx[k])
                    why[idx[k]] = "dohraya"
    if script is not None:
        lines = [dict(ln, n=norm(ln["text"])) for ln in script]
        ids = {id(w): i for i, w in enumerate(words)}
        takes, extras = pick_takes(words, lines)
        rep.append("== Best take (script se milan) ==")
        for i, ln in enumerate(lines):
            tk = takes.get(i)
            if not tk:
                rep.append(f"Scene {ln['scene']}: NAHI MILI -> \"{ln['text']}\" (line boli nahi, ya Whisper ne galat suna)")
                continue
            rep.append(f"Scene {ln['scene']}: {len(tk)} take")
            for t in tk:
                c0 = t["words"][0]
                tag = "RAKHA" if t["keep"] else "KATA "
                warn = "  (adhoori? sun ke dekho)" if t["keep"] and t["cov"] < 0.6 else ""
                rep.append(f"   {tag} {Path(src[c0['ci']]['file']).name} {c0['a']:.2f}-{t['words'][-1]['b']:.2f}s"
                           f"  milan {t['cov']:.0%}, filler {t['fill']}{warn}: {fmt(t['words'])}")
                if not t["keep"]:
                    for w in t["words"]:
                        if not w["lock"]:
                            drop.add(ids[id(w)])
                            why.setdefault(ids[id(w)], "retake")
        for ph in extras:
            c0 = ph[0]
            tag = "KATA " if args.drop_extra else "EXTRA"
            rep.append(f"   {tag} {Path(src[c0['ci']]['file']).name} {c0['a']:.2f}-{ph[-1]['b']:.2f}s"
                       f" script mein nahi: {fmt(ph)}")
            if args.drop_extra:
                for w in ph:
                    if not w["lock"]:
                        drop.add(ids[id(w)])
                        why.setdefault(ids[id(w)], "extra")
    small = [i for i in sorted(drop) if why.get(i) in ("filler", "dohraya")]
    if small:
        rep.append("== Filler / dohraya shabd kata ==")
        for i in small:
            w = words[i]
            rep.append(f"   {Path(src[w['ci']]['file']).name} {w['a']:.2f}s {why[i]}: {w['t']}")
    holes = {}
    for ci in {w["ci"] for w in words}:
        idx = [i for i, w in enumerate(words) if w["ci"] == ci]
        local = [words[i] for i in idx]
        pos = {g: k for k, g in enumerate(idx)}
        for r in runs(pos[i] for i in drop if i in pos):
            holes.setdefault(ci, []).append(hole(local, r))
    full = {ci for ci in {w["ci"] for w in words}
            if all(i in drop for i, w in enumerate(words) if w["ci"] == ci)}
    return holes, full, rep


def apply_words(regs, words, gap):
    """Regions ko pehle-aakhri shabd tak seemit karo, aur shabdon ke beech > gap wali khali jagah kaato."""
    if not words:
        return regs
    lo, hi = words[0][0] - 0.06, words[-1][1] + 0.1
    holes = [(b1 + 0.05, a2 - 0.05) for (_, b1), (a2, _) in zip(words, words[1:]) if a2 - b1 > gap + 0.12]
    out = []
    for a, b in regs:
        a, b = max(a, lo), min(b, hi)
        if b <= a:
            continue
        pieces = [(a, b)]
        for h0, h1 in holes:
            nxt = []
            for x, y in pieces:
                if h1 <= x or h0 >= y:
                    nxt.append((x, y))
                else:
                    if h0 > x:
                        nxt.append((x, h0))
                    if h1 < y:
                        nxt.append((h1, y))
            pieces = nxt
        out += pieces
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--db", type=float, default=-32, help="is se dheemi awaaz = khamoshi (default -32)")
    ap.add_argument("--gap", type=float, default=0.28, help="is se lambi khamoshi kaato (sec, default 0.28)")
    ap.add_argument("--pad", type=float, default=0.07, help="har tukde ke dono taraf saans (sec)")
    ap.add_argument("--min", type=float, default=0.18, help="is se chhota tukda = shor, hatao")
    ap.add_argument("--tail", type=float, default=0.12, help="clip ki aakhri line ke baad thoda ruk (sec)")
    ap.add_argument("--fps", type=int, default=30, help="video fps (tukde isi grid par)")
    ap.add_argument("--whisper", action="store_true", help="Whisper word timing se bhi kaato (room tone wali clips)")
    ap.add_argument("--fillers", action="store_true", help="aa/umm aur doharaye shabd kaato")
    ap.add_argument("--filler-words", help="aur filler, comma se (jaise \"मतलब,basically\")")
    ap.add_argument("--takes", action="store_true", help="script.md se milake har line ka best take rakho")
    ap.add_argument("--script", help="script.md (default: episode.json ke folder wala)")
    ap.add_argument("--drop-extra", action="store_true", help="script se na milne wala bola hua hissa bhi kaato")
    ap.add_argument("--model", help="Whisper model (default: --fillers/--takes par medium, warna small)")
    ap.add_argument("--dry-run", action="store_true", help="episode.json mat badlo, sirf report")
    args = ap.parse_args()
    if args.fillers or args.takes:
        args.whisper = True
    args.model = args.model or ("medium" if args.fillers or args.takes else "small")

    path = Path(args.episode)
    cfg = json.loads(path.read_text(encoding="utf-8"))
    src = cfg.get("clips_src") or cfg["clips"]
    cfg["clips_src"] = src
    holes, full, rep = {}, set(), []
    if args.fillers or args.takes:
        script = None
        if args.takes:
            sp = Path(args.script) if args.script else path.parent / "script.md"
            if not sp.exists():
                sys.exit(f"--takes ke liye script nahi mili: {sp}")
            script = script_lines(sp)
            if not script:
                sys.exit(f"{sp} mein koi 'Voice:' line nahi")
        holes, full, rep = plan_cuts(src, args, script)
    out, before, after = [], 0.0, 0.0
    for ci, c in enumerate(src):
        f = c["file"]
        start = float(c.get("start") or 0)
        dur = float(c.get("duration") or 0) or probe_dur(f) - start
        before += dur
        if c.get("nocut"):
            out.append(copy.deepcopy(c))
            after += dur
            continue
        if ci in full:
            print(f"  {Path(f).name}: poori clip retake/filler thi, hata di")
            continue
        regs = speech_regions(f, start, dur, args.db, args.gap)
        if args.whisper:
            ws = word_spans(f, start, dur, args.model)
            if ws is None:
                sys.exit("--whisper ke liye faster-whisper chahiye (.venv/bin/python se chalao)")
            regs = apply_words(regs, ws, args.gap)
        cuts = list(c.get("cuts", [])) + holes.get(ci, [])
        for h0, h1 in cuts:
            nxt = []
            for x, y in regs:
                if h1 <= x or h0 >= y:
                    nxt.append((x, y))
                else:
                    if h0 > x:
                        nxt.append((x, h0))
                    if h1 < y:
                        nxt.append((h1, y))
            regs = nxt
        regs = [(a, b) for a, b in regs if b - a >= args.min]
        if not regs:
            print(f"  {Path(f).name}: awaaz nahi mili, clip waise hi rakhi")
            out.append(copy.deepcopy(c))
            after += dur
            continue
        # pad + merge overlapping
        padded = []
        for k, (a, b) in enumerate(regs):
            a = max(start, a - args.pad)
            b = min(start + dur, b + (args.tail if k == len(regs) - 1 else args.pad))
            # manual cut ke andar pad mat failao
            for h0, h1 in cuts:
                if h0 <= a + args.pad <= h1 + 1e-6:
                    a = h1
                if h0 - 1e-6 <= b - args.pad <= h1:
                    b = h0
            if padded and a <= padded[-1][1]:
                padded[-1] = (padded[-1][0], b)
            else:
                padded.append((a, b))
        card_t = float((c.get("card") or {}).get("media_start") or 0)
        # frame grid par align: har tukda poore frames ka ho, warna ~45 tukdon mein video
        # awaaz se khisak jaata hai (lip-sync aur captions bigadte hain)
        padded = [(round(a * args.fps) / args.fps, round(b * args.fps) / args.fps) for a, b in padded]
        padded = [(a, b) for a, b in padded if b - a >= 2 / args.fps]
        for k, (a, b) in enumerate(padded):
            seg = copy.deepcopy(c)
            seg["start"] = round(a, 4)
            seg["duration"] = round(b - a, 4)
            if k > 0:
                seg.pop("transition", None)
                if seg.get("layout") != "split":
                    # jump cut: zoom badlo taaki cut "edit" lage, galti nahi
                    seg["zoom"] = "tight" if k % 2 == 1 else None
                    if seg["zoom"] is None:
                        seg.pop("zoom")
            if seg.get("card") and seg["card"].get("media"):
                seg["card"]["media_start"] = round(card_t, 3)
            card_t += b - a
            out.append(seg)
            after += b - a
        print(f"  {Path(f).name}: {dur:.2f}s -> {sum(b - a for a, b in padded):.2f}s ({len(padded)} tukde)")
    if rep:
        (path.parent / "cut_report.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
        print("\n".join(rep))
        print(f"Report: {(path.parent / 'cut_report.txt').as_posix()}")
    if args.dry_run:
        print(f"Dry run: {before:.1f}s -> {after:.1f}s hota. episode.json nahi badla.")
        return
    cfg["clips"] = out
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Khamoshi kati: {before:.1f}s -> {after:.1f}s. Ab: python tools/flow_voice.py {path.as_posix()}")


if __name__ == "__main__":
    sys.exit(main())
