import sys, json
from PIL import Image, ImageDraw, ImageFont
BOLD="/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"; REG="/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
def F(p,s): return ImageFont.truetype(p,s)
def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def build(cfg,out):
    W=H=1024; img=Image.new("RGB",(W,H),(13,20,38)); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,148],fill=(198,32,48))
    d.text((40,20),"THE WORLD IN ONE PICTURE",font=F(BOLD,30),fill=(255,255,255))
    d.text((40,58),cfg["date"],font=F(BOLD,50),fill=(255,255,255))
    d.text((40,116),"The day's biggest stories, at a glance",font=F(REG,23),fill=(255,220,220))
    y=164
    d.rounded_rectangle([32,y,992,y+272],radius=18,fill=(245,166,35))
    d.text((64,y+22),cfg["lead_tag"],font=F(BOLD,26),fill=(60,35,0))
    yy=y+60
    for ln in wrap(d,cfg["lead_head"],F(BOLD,54),880): d.text((64,yy),ln,font=F(BOLD,54),fill=(20,20,20)); yy+=62
    yy+=4
    for ln in wrap(d,cfg["lead_cap"],F(REG,28),880): d.text((64,yy),ln,font=F(REG,28),fill=(40,30,10)); yy+=37
    stories=cfg["stories"]; y0=448; ch=168; gap=10
    pos=[(32+(i%2)*492, y0+(i//2)*(ch+gap), 460, ch) for i in range(4)]+[(32,y0+2*(ch+gap),960,144)]
    colors=[(70,130,230),(40,180,140),(170,110,240),(240,130,60),(110,190,90)]
    for i,(s,(cx,cy,cw,chh)) in enumerate(zip(stories,pos)):
        d.rounded_rectangle([cx,cy,cx+cw,cy+chh],radius=14,fill=(27,38,64),outline=colors[i],width=4)
        d.text((cx+20,cy+12),s["tag"],font=F(BOLD,21),fill=(140,200,255))
        yy=cy+42; hf=F(BOLD,27)
        for ln in wrap(d,s["head"],hf,cw-40)[:2]: d.text((cx+20,yy),ln,font=hf,fill=(255,255,255)); yy+=33
        yy+=4; cf=F(REG,20)
        for ln in wrap(d,s["cap"],cf,cw-40)[:2]: d.text((cx+20,yy),ln,font=cf,fill=(200,210,225)); yy+=25
    d.text((40,966),"Sources: "+cfg["sources"],font=F(REG,19),fill=(150,160,180))
    img.save(out,optimize=True); print(out)
cfg=json.load(open(sys.argv[1])); build(cfg,sys.argv[2])
