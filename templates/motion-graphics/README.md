# Motion graphics

## Abhi (kaam karta hai, tested)
`build_video.py` ye deta hai: crossfade/slide transitions, animated (fade) title overlays, captions. `transition.type` mein ffmpeg xfade ke naam chalte hain (fade, wipeleft, slideleft, circleopen, ...).

## Agla step (optional, pehle episodes ke baad)
Complex animations (animated lower-thirds, counters, charts, logo reveals) ke liye:
- **HyperFrames by HeyGen** connector (HTML se video render), jo tum pehle se chun chuke ho, ya
- **Remotion** (React se video, free for individuals; commercial licence terms khud check karo). Tum React developer ho, to yeh tumhare liye natural hai. Node chahiye.

Tareeka: motion graphic ko alag clip (`assets/broll/` ya `raw-clips/`) ki tarah render karo, phir `episode.json` mein clip ki tarah jodo.

Ye pehle 2-3 episodes ke baad banayenge, jab pata ho kaun si animation baar-baar chahiye.
