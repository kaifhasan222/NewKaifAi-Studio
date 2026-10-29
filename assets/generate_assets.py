import numpy as np, wave, subprocess, os
SR=44100
rng=np.random.default_rng(7)
def t(d): return np.linspace(0,d,int(SR*d),endpoint=False)
def env(n,a=0.005,r=0.1):
    e=np.ones(n); na=max(1,int(SR*a)); nr=max(1,int(SR*r))
    e[:na]=np.linspace(0,1,na); e[-nr:]=np.minimum(e[-nr:],np.linspace(1,0,nr)); return e
def lp(x,k):  # simple moving-average lowpass
    k=max(1,int(k)); return np.convolve(x,np.ones(k)/k,mode="same")
def hp(x,k): return x-lp(x,k)
def norm(x,peak=0.8): return x/(np.max(np.abs(x))+1e-9)*peak
def save(x,path):
    x=np.clip(x,-1,1); w=path.replace(".mp3",".wav")
    with wave.open(w,"wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((x*32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",w,"-codec:a","libmp3lame","-q:a","2",path],check=True); os.remove(w)

def whoosh(d,lo,hi):
    n=int(SR*d); x=rng.standard_normal(n)
    # sweep: blend of low and high-passed noise with rising envelope
    a=hp(lp(x,SR/hi),SR/lo); tt=np.linspace(0,1,n)
    amp=np.sin(np.pi*tt)**2
    return norm(a*amp)
save(whoosh(0.55,200,5000),"assets/sfx/whoosh-01.mp3")
save(whoosh(0.8,120,3000),"assets/sfx/whoosh-02.mp3")
# pop
tt=t(0.14); f=900*np.exp(-tt*18)+250
save(norm(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*28)),"assets/sfx/pop-01.mp3")
# click
n=int(SR*0.04); x=rng.standard_normal(n); save(norm(hp(x,12)*np.exp(-np.linspace(0,1,n)*9)),"assets/sfx/click-01.mp3")
# riser
d=1.6; tt=t(d); f=180+900*(tt/d)**2; ph=2*np.pi*np.cumsum(f)/SR
nz=lp(rng.standard_normal(len(tt)),6)
r=(0.6*np.sin(ph)+0.5*nz)*(tt/d)**1.5
save(norm(r*env(len(tt),0.02,0.05)),"assets/sfx/riser-01.mp3")
# hit
d=0.9; tt=t(d); f=110*np.exp(-tt*5)+45
body=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*5)
nz=lp(rng.standard_normal(len(tt)),4)*np.exp(-tt*30)
save(norm(body+0.5*nz),"assets/sfx/hit-01.mp3")
# notification ding
d=1.0; tt=t(d)
ding=(np.sin(2*np.pi*1318*tt)+0.5*np.sin(2*np.pi*1976*tt)+0.25*np.sin(2*np.pi*2637*tt))*np.exp(-tt*5)
save(norm(ding*env(len(tt),0.003,0.05),0.7),"assets/sfx/ding-01.mp3")
# soft transition swish
save(whoosh(0.4,300,2500)*0.6,"assets/sfx/soft-transition-01.mp3")

# ---- background music: chill pad + soft pluck + gentle beat, Am-F-C-G, 80 BPM, 8 bars (~24s) loop
bpm=80; beat=60/bpm; bar=4*beat; chords=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]*2  # midi
mf=lambda m:440*2**((m-69)/12)
n=int(SR*bar*len(chords)); out=np.zeros(n)
for i,ch in enumerate(chords):
    s=int(SR*bar*i); L=int(SR*bar); tt=np.arange(L)/SR
    pad=sum(np.sin(2*np.pi*mf(m)*tt)+0.3*np.sin(2*np.pi*mf(m)*2*tt) for m in ch)
    pad*=np.minimum(1,tt/0.8)*np.minimum(1,(bar-tt)/0.8)*0.18
    bass=np.sin(2*np.pi*mf(ch[0]-12)*tt)*0.35*np.exp(-((tt%beat))*1.5)
    out[s:s+L]+=pad+bass
    # pluck arpeggio on 8ths
    for k in range(8):
        m=ch[k%3]+12; st=int(SR*k*beat/2); dl=int(SR*0.45); tp=np.arange(dl)/SR
        pl=np.sin(2*np.pi*mf(m)*tp)*np.exp(-tp*7)*0.22
        if s+st+dl<=n: out[s+st:s+st+dl]+=pl
    # soft kick on beats 1 and 3, hat-ish tick on offbeats
    for k in (0,2):
        st=int(SR*k*beat); dl=int(SR*0.25); tp=np.arange(dl)/SR
        kick=np.sin(2*np.pi*np.cumsum(50+90*np.exp(-tp*30))/SR)*np.exp(-tp*14)*0.5
        if s+st+dl<=n: out[s+st:s+st+dl]+=kick
    for k in range(4):
        st=int(SR*(k*beat+beat/2)); dl=int(SR*0.04)
        tick=hp(rng.standard_normal(dl),8)*np.exp(-np.linspace(0,1,dl)*8)*0.06
        if s+st+dl<=n: out[s+st:s+st+dl]+=tick
cf=int(SR*0.05); out[:cf]*=np.linspace(0,1,cf); out[-cf:]*=np.linspace(1,0,cf)
save(norm(out,0.7),"assets/music/chill-tech-01.mp3")
print("done")
