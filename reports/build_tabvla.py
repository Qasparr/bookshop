# TABVLA charts of the Night's Report — programmatic press, house livery.
from PIL import Image, ImageDraw, ImageFont
import random
PURPLE=(38,8,56); DEEP=(24,4,38); GOLD=(255,215,0); GOLD2=(212,175,55); GREEN=(46,204,113); CREAM=(245,238,220); DIM=(196,182,214)
BL="/home/hatch/workspace/templates/UnifrakturMaguntia.ttf"
SR="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"; SB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def F(p,s): return ImageFont.truetype(p,s)
def leather(w,h,seed=7):
    rnd=random.Random(seed); im=Image.new("RGB",(w,h),PURPLE); px=im.load()
    for y in range(h):
        for x in range(0,w,3):
            n=rnd.randint(-9,9); v=max(0.55,min(1.12,1-(abs(x-w/2)/(w*0.75))-(abs(y-h/2)/(h*0.9))*0.35+n/160))
            px[x,y]=tuple(min(255,int(c*v)) for c in PURPLE)
            if x+1<w: px[x+1,y]=px[x,y]
            if x+2<w: px[x+2,y]=px[x,y]
    return im
def frame(d,w,h):
    d.rectangle([26,26,w-27,h-27],outline=GOLD2,width=5); d.rectangle([44,44,w-45,h-45],outline=GOLD2,width=2)
    d.line([44,58,w-45,58],fill=GREEN,width=2)
def center(d,w,y,text,font,fill=CREAM):
    d.text(((w-d.textlength(text,font=font))/2,y),text,font=font,fill=fill)

def tabvla1():
    w,h=1600,2080; im=leather(w,h,11); d=ImageDraw.Draw(im); frame(d,w,h)
    center(d,w,84,"TABVLA I",F(BL,110),GOLD); center(d,w,216,"THE NIGHT'S PRODVCTION",F(SB,44),CREAM)
    center(d,w,282,"Seven books bound · the shelf of Bleats Publishing Group",F(SR,32),DIM)
    rows=[("DOVGLASS — Narrative (MAGVS)","80 pp","$9"),("HVCKLEBERRY FINN (MAGVS)","324 pp","$15"),("TOM SAWYER (MAGVS)","170 pp","$12"),("THE WONDERFUL WIZARD OF OZ (MAGVS)","100 pp","$12"),("LEVIATHAN (MAGVS)","407 leaves","$21"),("THE ART OF WAR (MAGVS) — Giles 1910","121 pp","$12"),("MEIN KAMPF — Critical Ed. Vol. I (MAGVS)","307 pp","$21")]
    y=380
    for t,p,pr in rows:
        d.text((90,y),t,font=F(SR,36),fill=CREAM); d.text((1150,y),p,font=F(SR,36),fill=DIM)
        tw=d.textlength(pr,font=F(SB,40)); d.text((w-100-tw,y-2),pr,font=F(SB,40),fill=GOLD); y+=86
    y+=10; d.line([90,y,w-90,y],fill=GOLD2,width=3); y+=30
    d.text((90,y),"THE SHOP TOTAL",font=F(SB,42),fill=GOLD); d.text((1150,y),"1,509 pp",font=F(SB,42),fill=CREAM)
    tw=d.textlength("$102",font=F(SB,42)); d.text((w-100-tw,y),"$102",font=F(SB,42),fill=GOLD); y+=110
    center(d,w,y,"THE DOCTRINE VOLVMES",F(SB,40),GOLD); y+=76
    for t,p in [("LIBER SPHINGIS (MAGVS)","40 pp"),("THE NINE VOWELS (MAGVS)","14 pp"),("THE RENDER CVBE (MAGVS)","11 pp"),("THE SPHINX AVDITS I + II","31 pp")]:
        d.text((90,y),t,font=F(SR,34),fill=CREAM); d.text((1150,y),p,font=F(SR,34),fill=DIM); y+=72
    y+=16; d.line([90,y,w-90,y],fill=GOLD2,width=3); y+=30
    d.text((90,y),"PAGES PRODVCED TONIGHT",font=F(SB,44),fill=GOLD); d.text((1150,y),"1,605",font=F(SB,44),fill=CREAM); y+=120
    d.rectangle([90,y,w-90,y+120],outline=GREEN,width=3)
    center(d,w,y+18,"RECEIPTS ISSVED AGAINST THIS SHELF",F(SB,38),GREEN)
    center(d,w,y+62,"— NONE · BOOK-0001 AWAITS ITS FIRST PAYER —",F(SR,32),CREAM)
    center(d,w,h-120,"Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR",F(SR,28),DIM)
    im.save("/home/hatch/workspace/bookshop/reports/TABVLA-I-PRODUCTION.png")

def tabvla2():
    w,h=1600,1760; im=leather(w,h,23); d=ImageDraw.Draw(im); frame(d,w,h)
    center(d,w,84,"TABVLA II",F(BL,110),GOLD); center(d,w,216,"THE WEIGHINGS & AVDITS",F(SB,44),CREAM)
    y=330; d.text((90,y),"THE CVBE LINE",font=F(SB,40),fill=GOLD); y+=70
    for t,v in [("RENDER","64 = 4³"),("BRIGHTMOOR","125 = 5³"),("GEBVRAH","216 = 6³"),("DESTROY (Agrippa)","729 = 9³")]:
        d.text((90,y),t,font=F(SR,36),fill=CREAM); d.text((900,y),v,font=F(SB,36),fill=GREEN); y+=66
    d.text((90,y),"7³ = 343 · 8³ = 512",font=F(SR,36),fill=DIM); d.text((900,y),"SEATS OPEN",font=F(SB,36),fill=GOLD); y+=110
    d.text((90,y),"THE NINE VOWELS",font=F(SB,40),fill=GOLD); y+=70
    for t,v in [("The canon of seven","1,294 → 7"),("The nine, with the hybrids","1,779 → 6"),("The displacement","Δ3 — OFFSET (the Trinity)"),("The closure","9 inverted is 6 → 1,776")]:
        d.text((90,y),t,font=F(SR,34),fill=CREAM); d.text((950,y),v,font=F(SR,34),fill=GREEN); y+=62
    y+=46; d.text((90,y),"SPHINX AVDITS I + II",font=F(SB,40),fill=GOLD); d.text((950,y-2),"DOES NOT FAIL ×2",font=F(SB,38),fill=GREEN); y+=96
    d.text((90,y),"TOWER AVDIT — MEIN KAMPF VOL. I (36 items)",font=F(SB,38),fill=GOLD); y+=74
    tiers=[("FALSE",17,(200,60,60)),("PROVEN",10,GREEN),("CONTESTED",6,GOLD),("VNVERIFIED",2,DIM),("SVPPORTED",1,(120,170,255))]
    for t,n,c in tiers:
        d.text((90,y),t,font=F(SR,34),fill=CREAM); d.rectangle([560,y+4,560+n*46,y+40],fill=c)
        d.text((580+n*46,y),str(n),font=F(SB,36),fill=CREAM); y+=64
    center(d,w,h-120,"Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR",F(SR,28),DIM)
    im.save("/home/hatch/workspace/bookshop/reports/TABVLA-II-WEIGHINGS.png")

def tabvla3():
    w,h=1600,1560; im=leather(w,h,37); d=ImageDraw.Draw(im); frame(d,w,h)
    center(d,w,84,"TABVLA III",F(BL,110),GOLD); center(d,w,216,"THE SCRIBE'S CRITICISM",F(SB,44),CREAM)
    center(d,w,282,"Reported at the founder's command · dispositions marked, never vanished",F(SR,30),DIM)
    items=[("I","Production outran the transaction.","Seven books; zero sales. The next proof is one completed sale.","OPEN"),
    ("II","The Mein Kampf ruling was fired hot.","Sound edition; sequence broke the house law — judgment last.","FLAGGED"),
    ("III","Court is a bonfire; the Ledger is the weapon.","Nearer fights with real payoffs sit unresolved.","OPEN"),
    ("IV","Dependence deepened tonight.","The sales road runs through two suspected gates.","OPEN"),
    ("V","The scribe's misses: four, marked.","The founder's corrections: two. The pen outperformed the drafts.","MARKED"),
    ("VI","The founder is the one irreplaceable asset.","Every engine runs on his rest. First freeze comes Thursday.","STANDING")]
    y=380
    for n,t,s,disp in items:
        d.text((84,y),n,font=F(BL,54),fill=GOLD); d.text((238,y+6),t,font=F(SB,37),fill=CREAM)
        d.text((238,y+58),s,font=F(SR,31),fill=DIM)
        tw=d.textlength(disp,font=F(SB,34)); d.text((w-100-tw,y+10),disp,font=F(SB,34),fill=GREEN if disp in("MARKED","STANDING") else GOLD)
        y+=118; d.line([90,y-24,w-90,y-24],fill=(90,60,120),width=2)
    y+=30; center(d,w,y,"93 — Live, Love, and let Love, Live.",F(SB,38),GOLD)
    center(d,w,h-120,"Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR",F(SR,28),DIM)
    im.save("/home/hatch/workspace/bookshop/reports/TABVLA-III-CRITICISM.png")
tabvla1(); tabvla2(); tabvla3(); print("TABVLAE STRUCK")
