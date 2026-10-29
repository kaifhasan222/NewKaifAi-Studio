#!/usr/bin/env python3
"""
build_advanced.py - Pro Split-Screen + Circular Facecam Bubble + Motion Graphics Pipeline.
Usage:
    python tools/build_advanced.py
"""
import subprocess
from pathlib import Path

BASE = Path("episodes/ep001/base_synced.mp4")
MUSIC = Path("assets/music/chill-tech-01.mp3")
SFX_W1 = Path("assets/sfx/whoosh-01.mp3")
SFX_W2 = Path("assets/sfx/whoosh-02.mp3")
SFX_POP = Path("assets/sfx/pop-01.mp3")
SFX_DING = Path("assets/sfx/ding-01.mp3")

BROLL_STUDENT = Path("assets/broll/student-study-01.mp4")
MG_NOTEBOOK = Path("assets/broll/mg_notebooklm.mp4")
MG_PERPLEXITY = Path("assets/broll/mg_perplexity.mp4")
MG_GAMMA = Path("assets/broll/mg_gamma.mp4")
MG_CTA = Path("assets/broll/mg_cta.mp4")

MASK_IMG = Path("assets/graphics/circle_mask.png")
BORDER_IMG = Path("assets/graphics/circle_border.png")
DIVIDER_IMG = Path("assets/graphics/divider.png")

CAPTIONS = Path("episodes/ep001/captions.srt")
OVERLAYS_ASS = Path(".build_overlays.ass")
OUT = Path("output/ep001.mp4")
OUT.parent.mkdir(parents=True, exist_ok=True)

w, h = 1080, 1920
head = (
    f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\n\n"
    "[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
    "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,"
    "Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
    "Style: TopTitle,Arial,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,0,8,60,60,260,1\n\n"
    "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
    "Dialogue: 0,0:00:00.00,0:00:07.50,TopTitle,,0,0,0,,{\\fad(150,150)}3 FREE AI TOOLS FOR STUDENTS\n"
    "Dialogue: 0,0:00:07.50,0:00:15.00,TopTitle,,0,0,0,,{\\fad(150,150)}1. GOOGLE NOTEBOOKLM\n"
    "Dialogue: 0,0:00:15.00,0:00:23.00,TopTitle,,0,0,0,,{\\fad(150,150)}2. PERPLEXITY AI\n"
    "Dialogue: 0,0:00:23.00,0:00:31.00,TopTitle,,0,0,0,,{\\fad(150,150)}3. GAMMA.APP\n"
    "Dialogue: 0,0:00:31.00,0:00:40.20,TopTitle,,0,0,0,,{\\fad(150,150)}FOLLOW @NewKaifAi\n"
)
OVERLAYS_ASS.write_text(head, encoding="utf-8")

caption_style = (
    "Fontname=Arial,Fontsize=18,Bold=1,PrimaryColour=&H0000FFFF,"
    "OutlineColour=&H00000000,Outline=2.4,Shadow=1,Alignment=2,MarginV=110"
)

inputs = [
    "-i", str(BASE),
    "-i", str(BROLL_STUDENT),
    "-i", str(MG_NOTEBOOK),
    "-i", str(MG_PERPLEXITY),
    "-i", str(MG_GAMMA),
    "-i", str(MG_CTA),
    "-i", str(MASK_IMG),
    "-i", str(BORDER_IMG),
    "-i", str(DIVIDER_IMG),
    "-stream_loop", "-1", "-i", str(MUSIC),
    "-i", str(SFX_W1),
    "-i", str(SFX_W2),
    "-i", str(SFX_POP),
    "-i", str(SFX_DING)
]

vfilters = [
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[vbase]",
    "[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1,fps=30[spl_top]",
    "[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1,fps=30[spl_bot]",
    "[spl_top][spl_bot]vstack[spl_stack]",
    "[spl_stack][8:v]overlay=0:950[v_split]",
    "[0:v]crop=520:520:100:150,scale=340:340,format=yuva420p[face_sq]",
    "[6:v]scale=340:340[cmask]",
    "[7:v]scale=340:340[cborder]",
    "[face_sq][cmask]alphamerge[face_circ]",
    "[face_circ][cborder]overlay=0:0[face_bubble]",
    "[vbase][v_split]overlay=0:0:enable='between(t,2.2,7.5)'[v_s1]",
    "[v_s1][2:v]overlay=0:0:enable='between(t,10.0,15.0)'[v_s2]",
    "[v_s2][3:v]overlay=0:0:enable='between(t,18.0,23.0)'[v_s3]",
    "[v_s3][4:v]overlay=0:0:enable='between(t,26.0,31.0)'[v_s4]",
    "[v_s4][5:v]overlay=0:0:enable='between(t,34.5,40.2)'[v_s5]",
    "[v_s5][face_bubble]overlay=690:1340:enable='between(t,10.0,15.0)+between(t,18.0,23.0)+between(t,26.0,31.0)+between(t,34.5,40.2)'[v_with_face]",
    f"[v_with_face]subtitles={OVERLAYS_ASS.as_posix()},subtitles={CAPTIONS.as_posix()}:force_style='{caption_style}'[vout]"
]

fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
sfx_schedule = [
    (10, 2200),
    (12, 7500),
    (11, 10000),
    (12, 15000),
    (10, 18000),
    (12, 23000),
    (11, 26000),
    (12, 31000),
    (13, 34500)
]

sfx_filters = []
mix_inputs = ["[vo]", "[mud]"]

for idx, (inp, delay_ms) in enumerate(sfx_schedule):
    sfx_filters.append(f"[{inp}:a]{fmt},volume=0.75,adelay={delay_ms}|{delay_ms}[s{idx}]")
    mix_inputs.append(f"[s{idx}]")

afilters = [
    f"[0:a]{fmt},apad,asplit=2[vo][vsc]",
    f"[9:a]{fmt},volume=0.09[mu]",
    "[mu][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=450[mud]",
] + sfx_filters

num_mix = len(mix_inputs)
mix_str = "".join(mix_inputs)
afilters.append(f"{mix_str}amix=inputs={num_mix}:duration=first:dropout_transition=0,volume={num_mix},loudnorm=I=-16:TP=-1.5:LRA=11[aout]")

filter_complex = ";".join(vfilters + afilters)

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[vout]", "-map", "[aout]",
    "-t", "40.2",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    str(OUT)
]

def main():
    print("Rendering Master Video...")
    subprocess.run(cmd, check=True)
    print("Done! Rendered to", OUT)

if __name__ == "__main__":
    main()
