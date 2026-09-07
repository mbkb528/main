import os, io, math, textwrap, requests
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

OUT='italy_trip_2026.pdf'
TMP='italy-trip/assets'
os.makedirs(TMP,exist_ok=True)

items=[
 dict(title='Florence',tags='FULL DAY · TUSCANY',img='https://upload.wikimedia.org/wikipedia/commons/7/77/Florence_Duomo_from_Michelangelo_hill.jpg',body='The ambitious day, but worthwhile. Think Duomo area, Piazza della Signoria, Ponte Vecchio, a good lunch and one optional museum or neighborhood wander. Trying to conquer Florence with two toddlers would be the mistake; seeing a strong slice of it is the win.',links=[('Florence guide','https://www.feelflorence.it/en')]),
 dict(title='Montepulciano + Pienza + Lupaia',tags='FULL DAY · VAL D\'ORCIA',img='https://www.eurocasa.com/media/tuscany-tips/144_shutterstock_2393932499bis.jpg',body='A strong countryside day and already a great family idea: Montepulciano for the hill town and wine, Pienza for the Renaissance center and Val d\'Orcia views, and Lupaia because it has personal meaning to the group. Three stops is enough.',links=[('Montepulciano','https://www.visittuscany.com/en/towns-and-villages/montepulciano/'),('Lupaia','https://www.lupaia.com/en/')]),
 dict(title='Gubbio',tags='MEDIEVAL · SPECIAL TIMING',img='https://www.italyonair.com/images/italyonair/luoghi/umbria/gubbio/gubbio.png',body='One of the best medieval-town outings from the villa, and the trip overlaps the Festival del Medioevo on Sept. 23-27. The festival can simply add atmosphere to a day of piazzas, wandering and lunch.',links=[('Festival del Medioevo','https://www.festivaldelmedioevo.it/'),('Gubbio guide','https://www.italia.it/en/umbria/perugia/gubbio/piazza-grande')]),
 dict(title='Lake Trasimeno + Castiglione del Lago',tags='LAKE · EASY PACE',img='https://travel.thewom.it/content/uploads/sites/4/2026/03/castiglione-del-lago-704x528.jpg',body='A useful change from hill towns: old center, fortress, lake views, long lunch and waterfront time. A boat is optional only if everybody is still thriving. Easy to shorten without ruining the day.',links=[('Lake & Castiglione guide','https://www.italia.it/en/umbria/things-to-do/castiglione-del-lago')]),
 dict(title='Umbertide + Montone',tags='NEARBY · LOW COMMITMENT',img='https://www.provincia.perugia.it/sites/default/files/2021-09/montone218325331_3994474800675540_1295676405043348123_n_0.jpg',body='The pressure-release option. Coffee or market in Umbertide, then Montone for wandering, lunch or an aperitivo. Close enough that this can be a morning, post-nap outing or simply the answer to “we should do something.”',links=[('Umbertide','https://www.umbriatourism.it/en/umbertide'),('Montone','https://www.umbriatourism.it/en/montone')]),
 dict(title='Cortona',tags='TUSCANY · FLEXIBLE',img='https://cdn-thumbs.ohmyprints.net/1/dc0ca64811d172c759d956fa5734eb91/817x600/thumbnail/fit.jpg',body='An easier taste of Tuscany than Florence. Wander the historic center, have lunch, take in the views and head home. A very good substitute on a day when the group wants something beautiful without an expedition.',links=[('Cortona guide','https://www.visittuscany.com/en/towns-and-villages/cortona/')]),
 dict(title='Assisi',tags='MAJOR SIGHT · 800TH ANNIVERSARY',img='https://www.ameliaonline.it/immagini/basilica-convento-san-francesco-assisi-umbria.jpg',body='The strongest “big Umbrian” alternative. The Basilica of St. Francis, old town and views are plenty for one day. 2026 marks 800 years since St. Francis\'s death, so the visit carries extra significance during this trip.',links=[('Visit Assisi','https://www.visit-assisi.it/en/')]),
 dict(title='Perugia',tags='CITY · GOOD SUBGROUP',img='https://rossiwrites.com/wp-content/uploads/2023/03/The-Fontana-Maggiore-seen-from-Palazzo-dei-Priori-Perugia-Italy-rossiwrites.com-2-1024x681.jpg.webp',body='More city energy, architecture, shops and museums than the smaller towns. It is less stroller-simple, which is exactly why it may work better for whichever adults really want a city afternoon rather than all ten people moving together.',links=[('Perugia guide','https://www.umbriatourism.it/en/perugia')]),
 dict(title='Città di Castello',tags='VERY CLOSE · HALF DAY',img='https://image.jimcdn.com/app/cms/image/transf/none/path/sef2acf15629609b3/image/i1a9aa1d49a77aedf/version/1721558326/image.jpg',body='One of the easiest genuine town outings from the villa. Historic center, cafés and local shops, with Alberto Burri\'s collections available for anyone interested in modern art.',links=[('Città di Castello guide','https://www.umbriatourism.it/en/citta-di-castello')]),
 dict(title='Spello',tags='SCENIC · OPTIONAL',img='https://media.istockphoto.com/id/1029350904/photo/spello-medieval-town.jpg?s=612x612&w=0&k=20&c=LzlwQY5AXnIeFOktwAoXV4qobFxHE96mwq7mL5kder4=',body='A compact pink-stone hill town famous for flower-lined alleys, Roman remains and Pinturicchio. It can stand alone for a relaxed outing or pair with Assisi for a smaller subgroup wanting a fuller sightseeing day.',links=[('Spello guide','https://www.umbriatourism.it/en/spello')]),
 dict(title='Passignano sul Trasimeno',tags='LAKE · ALTERNATIVE',img='https://www.cortonatouristguide.com/assets/images/tours/lago-trasimeno-passignano/02.jpg',body='The looser lake alternative: waterfront promenade, lunch, boats and room to move around. Pick Passignano or Castiglione depending on mood; there is no reason to force both.',links=[('Passignano guide','https://www.umbriatourism.it/en/passignano-sul-trasimeno')]),
 dict(title='Golf at Antognolla',tags='HALF DAY · GOLF',img='https://borgoildolcefarniente.com/assets/components/phpthumbof/cache/antognolla-golfbaan.a9ab7863f928f6d4abf786199c5d68bf.jpg',body='The obvious golf choice. Early tee time, 18 holes and lunch if desired, with a realistic shot at being back mid-afternoon. The course sits beneath a medieval castle and is scenic enough to justify the outing on its own.',links=[('Antognolla Golf','https://www.antognolla.com/golf/the-course')]),
 dict(title='Truffle hunt',tags='2-3 HOURS · VERY UMBRIAN',img='https://www.homeinitaly.com/_data/magazine/articles/2020-03-truffle-hunting-in-umbria/truffle-hunting-in-umbria-4-trufflehunting.jpg',body='A smaller-group experience that actually feels specific to the region: guide, dog, woods, then something edible at the end. Better for whoever is excited about it than as an all-ten-person obligation.',links=[('Umbria truffles','https://www.umbriatourism.it/en/truffle')]),
 dict(title='Winery / tasting',tags='FLEXIBLE · ADULTS',img='https://www.winetourism.com/files/2025/04/k1m0150_web.jpg',body='Easy to keep this small. Choose a producer near Umbertide/Niccone or simply fold wine into the Montepulciano day. One good tasting is better than adding an entire extra day of driving for wine.',links=[('Umbria food & wine','https://www.umbriatourism.it/en/food-and-wine')]),
 dict(title='Farm / animals / countryside morning',tags='TODDLER-CENTERED · LOW STAKES',img='https://umbriabimbo.it/wp-content/uploads/2023/02/Agriturismo-la-Fattoria-Didattica-di-Monte-Castello-di-Vibio.jpg',body='At least one outing should exist because the toddlers would enjoy it, not because adults feel obligated to see another masterpiece. Animals, an agriturismo or a simple countryside visit gives everybody a lower-stakes morning.',links=[('Family farm ideas','https://umbriabimbo.it/agriturismi-famiglie-bambini-umbria/')]),
 dict(title='Nearby grown-up escapes',tags='AFTER BEDTIME · CLOSE TO HOME',img='https://www.ristorantealchimista.it/wp-content/uploads/2022/02/237PPMF2492.jpg',body='When the grandparents are at the villa and the monitors are covered, the best evening move is probably not another major destination. Montone is the atmospheric choice for wine and dinner; Umbertide is the low-logistics option; and Calagrana is especially appealing because it is right in the Spedalicchio area.',links=[('Montone dinner idea','https://www.ilcapitano.com/en/'),('Umbertide restaurants','https://www.google.com/maps/search/restaurants+Umbertide+Italy'),('Calagrana','https://www.calagrana.com/')])
]

headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36','Accept':'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'}

def download(url, idx):
    ext='.jpg'
    p=os.path.join(TMP,f'{idx:02d}{ext}')
    r=requests.get(url,headers=headers,timeout=35,allow_redirects=True)
    r.raise_for_status()
    if len(r.content)<5000: raise RuntimeError(f'too small {len(r.content)}')
    im=Image.open(io.BytesIO(r.content)).convert('RGB')
    im.thumbnail((1800,1200),Image.Resampling.LANCZOS)
    im.save(p,'JPEG',quality=88,optimize=True)
    return p

for i,it in enumerate(items):
    try:
        it['path']=download(it['img'],i)
        print('OK',i,it['title'],it['path'])
    except Exception as e:
        print('FAIL',i,it['title'],e)
        it['path']=None

W,H=letter
INK=HexColor('#26352d'); CREAM=HexColor('#f5efe4'); PAPER=HexColor('#fffdf8'); GOLD=HexColor('#bd9455'); MUTED=HexColor('#66716a'); TAG=HexColor('#e8e3d4')
c=canvas.Canvas(OUT,pagesize=letter)
c.setTitle('Umbria + Tuscany Family Ideas - 2026')

def cover_image(path):
    if not path:return
    im=Image.open(path); iw,ih=im.size
    boxw,boxh=W,H
    scale=max(boxw/iw,boxh/ih); sw,sh=iw*scale,ih*scale
    x=(W-sw)/2;y=(H-sh)/2
    c.drawImage(ImageReader(im),x,y,sw,sh,mask='auto')

def draw_cover():
    bg=next((x['path'] for x in items if x['title'].startswith('Montepulciano') and x['path']),None) or next((x['path'] for x in items if x['path']),None)
    c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
    cover_image(bg)
    c.setFillColor(HexColor('#18251f'));c.setFillAlpha(.68);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillAlpha(1)
    c.setFillColor(white);c.setFont('Helvetica-Bold',10);c.drawString(42,H-64,'SEPTEMBER 22 - OCTOBER 3, 2026  ·  UMBRIA + TUSCANY')
    c.setFont('Times-Bold',38);c.drawString(42,170,'Things We Could Do')
    c.setFont('Times-Roman',16);txt='A loose menu of day trips, small adventures and grown-up escapes from Spedalicchio. Not an itinerary. Definitely not a checklist.'
    y=140
    for line in textwrap.wrap(txt,58): c.drawString(42,y,line); y-=20
    c.showPage()

def fit_image(path,x,y,w,h):
    if not path:
        c.setFillColor(HexColor('#ddd7ca'));c.rect(x,y,w,h,fill=1,stroke=0);return
    im=Image.open(path); iw,ih=im.size
    scale=max(w/iw,h/ih); sw,sh=iw*scale,ih*scale
    # crop in pixel space for cover fit
    cx=max(0,(sw-w)/2/scale); cy=max(0,(sh-h)/2/scale)
    cw=w/scale; ch=h/scale
    crop=im.crop((int(cx),int(cy),int(cx+cw),int(cy+ch)))
    c.drawImage(ImageReader(crop),x,y,w,h,mask='auto')

def draw_button(label,url,x,y):
    fs=9.5; pad=10; bh=24
    bw=stringWidth(label,'Helvetica-Bold',fs)+2*pad
    c.setStrokeColor(INK);c.setLineWidth(.8);c.roundRect(x,y,bw,bh,12,fill=0,stroke=1)
    c.setFillColor(INK);c.setFont('Helvetica-Bold',fs);c.drawString(x+pad,y+7,label)
    c.linkURL(url,(x,y,x+bw,y+bh),relative=0,thickness=0)
    return bw

def draw_card(it, x, y, w, h):
    c.setFillColor(PAPER);c.roundRect(x,y,w,h,16,fill=1,stroke=0)
    img_h=150
    # image region clipped by page shape is okay, rounded corner visual not essential
    fit_image(it['path'],x,y+h-img_h,w,img_h)
    px=x+18; py=y+h-img_h-22
    c.setFillColor(TAG); tagw=min(w-36,stringWidth(it['tags'],'Helvetica-Bold',8)+18)
    c.roundRect(px,py-3,tagw,19,9,fill=1,stroke=0)
    c.setFillColor(INK);c.setFont('Helvetica-Bold',8);c.drawString(px+9,py+3,it['tags'])
    py-=35
    c.setFont('Times-Bold',18);c.setFillColor(INK)
    title_lines=textwrap.wrap(it['title'],34)
    for ln in title_lines[:2]: c.drawString(px,py,ln);py-=20
    py-=2
    c.setFont('Times-Roman',10.5);c.setFillColor(INK)
    body_lines=textwrap.wrap(it['body'],58)
    for ln in body_lines[:7]: c.drawString(px,py,ln);py-=14
    by=y+14; bx=px
    for label,url in it['links']:
        bw=draw_button(label,url,bx,by)
        bx+=bw+7
        if bx>x+w-100: by+=28;bx=px

def draw_intro():
    c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(INK);c.setFont('Times-Bold',28);c.drawString(42,H-72,'A loose menu, not a schedule')
    c.setFont('Times-Roman',14);y=H-112
    intro='With two 14-month-olds and eight adults, the best outings are the ones that feel worth leaving the villa for without consuming the whole trip. Most of these can be done at a comfortable pace and still get everybody back for dinner with the toddlers before bedtime.'
    for line in textwrap.wrap(intro,76): c.drawString(42,y,line);y-=19
    y-=14;c.setStrokeColor(GOLD);c.setLineWidth(3);c.line(42,y,42,y-96)
    c.setFont('Times-Bold',13);c.drawString(58,y-4,'The idea')
    c.setFont('Times-Roman',12);note='Keep Florence and the Montepulciano-Pienza-Lupaia day as the bigger anchors, then pull from the Umbrian options whenever weather, naps and collective enthusiasm line up.'
    yy=y-26
    for line in textwrap.wrap(note,72): c.drawString(58,yy,line);yy-=17
    yy-=18;c.setFont('Times-Italic',12);c.setFillColor(MUTED)
    c.drawString(42,yy,'If half of this guide goes untouched because everyone is enjoying the villa, the trip is working.')
    c.showPage()

draw_cover();draw_intro()
card_w=W-84; card_h=332; x=42; top=H-42
for idx,it in enumerate(items):
    if idx%2==0:
        c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
        y1=top-card_h
        draw_card(it,x,y1,card_w,card_h)
    else:
        y2=42
        draw_card(it,x,y2,card_w,card_h)
        c.showPage()
if len(items)%2==1:c.showPage()

# final credits/source page
c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(INK);c.setFont('Times-Bold',24);c.drawString(42,H-66,'Photo & link notes')
c.setFont('Times-Roman',9.5);y=H-94
for it in items:
    src=it['img']
    line=f"{it['title']}: {src}"
    for j,ln in enumerate(textwrap.wrap(line,95)):
        if y<55:c.showPage();c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Times-Roman',9.5);y=H-55
        c.drawString(42,y,ln); y-=12
    y-=3
c.save()
print('WROTE',OUT,os.path.getsize(OUT))
