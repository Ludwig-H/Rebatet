#!/usr/bin/env python3
"""Cartes SVG et atlas HTML autonomes. Python >= 3.10, bibliothèque standard.
Entrées : 04_Donnees/lieux.json, fond_osm.geojson. Aucun accès réseau.
Projection locale équirectangulaire, latitude de référence 45.76°.
"""
from pathlib import Path
import math,json,html,textwrap,hashlib
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'04_Donnees';OUT=ROOT/'05_Cartes'
COS=math.cos(math.radians(45.76))
COL={'atteste':'#235460','probable':'#b07125','hypothese':'#b45942','non_localise':'#7a7772'}
LAB={'atteste':'Localisation identifiée','probable':'Localisation probable','hypothese':'Hypothèse à vérifier','non_localise':'Non localisé'}
PAPER='#f7f2e8';INK='#243a3f';MUTED='#687778';WATER='#afcbd0'
esc=lambda s:html.escape(str(s),quote=True)

def normalise(rows):
 if isinstance(rows,dict):rows=rows.get('lieux',rows.get('features',[]))
 out=[]
 for i,r in enumerate(rows):
  if r.get('type')=='Feature':r={**r.get('properties',{}),'geometry':r.get('geometry')}
  r=dict(r);r['nom']=r.get('nom',r.get('name',r.get('label',r.get('id',str(i)))))
  r['statut']=r.get('statut','non_localise');r['description']=r.get('description',r.get('note',''))
  r['rang']=i+1;r['num']=r.get('code') or str(i+1);r.setdefault('id',str(i+1));r.setdefault('refs',[]);r.setdefault('sources',[])
  out.append(r)
 return out

def flatcoords(g):
 if not g:return []
 t=g.get('type');c=g.get('coordinates',[])
 if t=='Point':return [c]
 if t=='LineString':return c
 if t=='Polygon':return c[0] if c else []
 if t=='MultiLineString':return [p for line in c for p in line]
 if t=='MultiPolygon':return [p for poly in c for p in poly[0]]
 return []

def anchor(g):
 c=flatcoords(g)
 if not c:return None
 if g['type']=='LineString':
  lengths=[math.hypot((q[0]-p[0])*COS,q[1]-p[1]) for p,q in zip(c,c[1:])]
  target=sum(lengths)/2;sofar=0
  for p,q,length in zip(c,c[1:],lengths):
   if sofar+length>=target:
    t=(target-sofar)/length if length else 0
    return [p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])]
   sofar+=length
  return c[0]
 if g['type']=='Polygon' and len(c)>1 and c[0]==c[-1]:c=c[:-1]
 return [sum(p[0] for p in c)/len(c),sum(p[1] for p in c)/len(c)]

def inside(p,b):return bool(p and b[0]<=p[0]<=b[2] and b[1]<=p[1]<=b[3])

def projector(b,x,y,w,h):
 gw=(b[2]-b[0])*COS;gh=b[3]-b[1];s=min(w/gw,h/gh)
 ox=x+(w-gw*s)/2;oy=y+(h-gh*s)/2
 def proj(p):return (ox+(p[0]-b[0])*COS*s,oy+(b[3]-p[1])*s)
 return proj,s/111195

def pathline(coords,pr,close=False):
 return ' '.join(('M' if i==0 else 'L')+f'{pr(p)[0]:.1f},{pr(p)[1]:.1f}' for i,p in enumerate(coords))+(' Z' if close else '')

def geometry_path(g,pr):
 if not g:return ''
 t=g['type'];c=g['coordinates']
 if t=='LineString':return pathline(c,pr)
 if t=='Polygon':return ' '.join(pathline(r,pr,True) for r in c)
 if t=='MultiLineString':return ' '.join(pathline(r,pr) for r in c)
 if t=='MultiPolygon':return ' '.join(pathline(r,pr,True) for poly in c for r in poly)
 return ''

def overlaps(g,b):
 cs=flatcoords(g)
 return bool(cs and min(p[0] for p in cs)<=b[2] and max(p[0] for p in cs)>=b[0] and min(p[1] for p in cs)<=b[3] and max(p[1] for p in cs)>=b[1])

def base_svg(features,b,pr,zoom=False):
 chunks=[]
 for kind in ['park','water','river','road']:
  for f in features:
   p=f['properties'];g=f['geometry']
   if p['kind']!=kind or not overlaps(g,b):continue
   path=geometry_path(g,pr)
   if kind=='park':chunks.append(f'<path d="{path}" fill="#dce4d2" stroke="none"/>')
   elif kind=='water':chunks.append(f'<path d="{path}" fill="{WATER}" fill-rule="evenodd" stroke="none"/>')
   elif kind=='river':
    # Centre lines only; actual width comes from natural=water polygons.
    chunks.append(f'<path d="{path}" fill="none" stroke="{WATER}" stroke-width="3"/>')
   else:
    h=p.get('highway','');wide=h in ['primary','secondary','tertiary','trunk','motorway']
    width=(3.0 if wide else 1.05)*(1.35 if zoom else 1)
    color='#fffdf7' if wide else '#e3ddce'
    chunks.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width:.2f}" stroke-linejoin="round"/>')
 return ''.join(chunks)

def symbol(x,y,num,status,size=15):
 color=COL.get(status,COL['non_localise'])
 if status=='probable':s=f'<rect x="{x-size}" y="{y-size}" width="{2*size}" height="{2*size}" rx="3" transform="rotate(45 {x} {y})" fill="{color}" stroke="{PAPER}" stroke-width="2.2"/>'
 elif status=='hypothese':s=f'<circle cx="{x}" cy="{y}" r="{size}" fill="{PAPER}" stroke="{color}" stroke-width="2.5" stroke-dasharray="4 2"/>'
 else:s=f'<circle cx="{x}" cy="{y}" r="{size}" fill="{color}" stroke="{PAPER}" stroke-width="2.2"/>'
 textcolor=color if status=='hypothese' else 'white'
 fs=12.5 if len(str(num))<=2 else round(size*0.68,1)
 return s+f'<text x="{x}" y="{y+fs*0.36:.1f}" text-anchor="middle" fill="{textcolor}" font-size="{fs}" font-weight="700">{num}</text>'

def map_marks(rows,b,pr,mpp,static=True):
 result=[];placed=[]
 for r in rows:
  g=r.get('geometry');a=anchor(g)
  if not inside(a,b):continue
  x,y=pr(a);status=r['statut'];col=COL.get(status,COL['non_localise']);path=geometry_path(g,pr)
  shape='';typ=g['type']
  if typ=='Point':
   rad=max(0,float(r.get('precision_m') or 0))*mpp
   if status!='atteste' or rad>12:
    rad=max(rad,18);shape=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-width="1.1" stroke-dasharray="4 3"/>'
  elif typ in ['LineString','MultiLineString'] and r.get('categorie')=='voie':
   # rue nommée : un filet, non une bande d'incertitude
   shape=f'<path d="{path}" stroke="#fffdf8" stroke-width="5" opacity=".8" fill="none" stroke-linecap="round"/><path d="{path}" stroke="{col}" stroke-width="2.4" opacity=".75" fill="none" stroke-linecap="round"/>'
  elif typ in ['LineString','MultiLineString']:
   # tronçon de recherche le long d'une voie : la largeur reste symbolique (precision_m mesure la position le long de la voie)
   width=max(8,min(16,float(r.get('precision_m') or 35)*2*mpp))
   shape=f'<path d="{path}" stroke="{col}" stroke-width="{width:.1f}" opacity=".14" fill="none" stroke-linecap="round"/><path d="{path}" stroke="{col}" stroke-width="2.2" stroke-dasharray="5 4" fill="none"/>'
  else:shape=f'<path d="{path}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 4"/>'
  # A number is a callout, not a spurious geocoded address.
  lx,ly=x,y
  if typ!='Point':lx+=25;ly-=20
  if static:
   for step in range(20):
    if all((lx-px)**2+(ly-py)**2>36**2 for px,py in placed):break
    angle=step*2.39996;rad=24+step*4;lx=x+rad*math.cos(angle);ly=y+rad*math.sin(angle)
  placed.append((lx,ly))
  connector=f'<path d="M{x:.1f},{y:.1f} L{lx:.1f},{ly:.1f}" stroke="{col}" stroke-width="1.2" fill="none"/>' if abs(lx-x)+abs(ly-y)>5 else ''
  result.append(f'<g class="lieu" data-id="{esc(r["id"])}" data-status="{status}" tabindex="0" role="button" aria-label="{esc(r["nom"])}"><title>{esc(r["nom"])} — {esc(LAB.get(status,status))}</title>{shape}{connector}{symbol(round(lx,1),round(ly,1),r["num"],status,12 if r.get('categorie')=='voie' else 15)}</g>')
 return ''.join(result)

def texts(x,y,lines,size=16,color=INK,step=None,**attrs):
 step=step or size*1.45
 extra=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
 return ''.join(f'<text x="{x}" y="{y+i*step}" fill="{color}" font-size="{size}" {extra}>{esc(line)}</text>' for i,line in enumerate(lines))

def wrapped(s,width):return textwrap.wrap(str(s),width,break_long_words=False,break_on_hyphens=False)

def annotations(b,pr,zoom):
 out=[]
 if zoom:
  labels=[('LE RHÔNE',[4.8390,45.7598],-80,19),('COURS LAFAYETTE',[4.8483,45.76375],-4,12),('AVENUE DE SAXE',[4.8455,45.7598],-82,12),('RUE DE CRÉQUI',[4.8476,45.7607],-82,12),('COURS GAMBETTA',[4.8457,45.7548],-6,12),('LA GUILLOTIÈRE',[4.8428,45.7518],0,18)]
 else:
  labels=[('LE RHÔNE',[4.8404,45.7696],-68,20),('LA SAÔNE',[4.8248,45.7494],-55,18),('FOURVIÈRE',[4.8172,45.7627],0,15),('PRESQU’ÎLE',[4.8334,45.7577],-81,15),('LES BROTTEAUX',[4.8525,45.7734],0,15),('LA GUILLOTIÈRE',[4.8497,45.7485],0,15),('LA CROIX-ROUSSE',[4.8274,45.7767],0,15)]
 for name,p,rot,size in labels:
  if not inside(p,b):continue
  x,y=pr(p);out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" transform="rotate({rot} {x:.1f} {y:.1f})" fill="#6c8586" font-size="{size}" letter-spacing="2" font-weight="500">{esc(name)}</text>')
 return ''.join(out)

def static_svg(rows,features,b,title,subtitle,zoom,filename):
 selected=[r for r in rows if inside(anchor(r.get('geometry')),b) and r.get('carte_principale',r.get('principal',True))]
 # An intentional editorial selection; all records remain accessible in the atlas.
 selected=sorted(selected,key=lambda r:(r.get('priorite',r.get('priority',50)),r['rang']))[:18]
 if not zoom:
  for extra_id in ['mere_brazier','lugdunum']:
   found=next((r for r in rows if r['id']==extra_id and inside(anchor(r.get('geometry')),b)),None)
   if found and all(r['id']!=extra_id for r in selected):selected.append(found)
 selected=sorted(selected,key=lambda r:r['num'])
 x,y,w,h=54,230,1000,920;pr,mpp=projector(b,x+22,y+22,w-44,h-44)
 p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1280" viewBox="0 0 1600 1280" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}. Fond contemporain OpenStreetMap. Localisations identifiées, probables et hypothétiques distinguées.</desc><defs><clipPath id="clip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath></defs><rect width="1600" height="1280" fill="{PAPER}"/><g font-family="Arial, Helvetica, sans-serif">']
 p.append(texts(58,62,['LES DEUX ÉTENDARDS · ATLAS CRITIQUE'],16,MUTED,letter_spacing='3'))
 p.append(f'<text x="54" y="137" font-family="Georgia, serif" font-size="62" fill="{INK}">{esc(title)}</text>')
 p.append(texts(58,184,[subtitle],20,MUTED))
 p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#ece9de"/><g clip-path="url(#clip)">{base_svg(features,b,pr,zoom)}{annotations(b,pr,zoom)}{map_marks(selected,b,pr,mpp)}</g>')
 # north arrow and scale are in modern metric ground distance.
 p.append(f'<g transform="translate({x+55} {y+65})"><path d="M0,-23 L-8,5 L0,0 L8,5 Z" fill="{INK}"/><text x="0" y="-32" text-anchor="middle" font-size="14" fill="{INK}">N</text></g>')
 scale_m=250 if zoom else 1000;sw=scale_m*mpp;sx=x+35;sy=y+h-32
 p.append(f'<path d="M{sx},{sy-6} V{sy} H{sx+sw:.1f} V{sy-6}" stroke="{INK}" stroke-width="2" fill="none"/>'+texts(sx,sy-13,[f'{scale_m} m'],13,INK))
 p.append(texts(1090,258,['LIEUX & DEGRÉS DE CERTITUDE'],15,MUTED,letter_spacing='1.4'))
 ry=302
 for status in ['atteste','probable','hypothese']:
  p.append(symbol(1105,ry-3,'',status,9));p.append(texts(1127,ry+3,[LAB[status]],16,INK));ry+=31
 p.append(texts(1090,421,['Sélection de lieux ; toutes les notices dans l’atlas.', 'Une zone ne désigne pas une adresse.'],15,MUTED))
 ry=490
 for r in selected:
  name=wrapped(r.get('carte_nom',r['nom'].split(' — ')[0]),43)
  p.append(symbol(1105,ry-4,r['num'],r['statut'],12));p.append(texts(1134,ry,name,16,INK,step=21))
  ry+=max(28 if not zoom else 32,21*len(name)+6)
 p.append(f'<line x1="1090" y1="{min(ry+15,1120)}" x2="1540" y2="{min(ry+15,1120)}" stroke="#ccc6b6"/>')
 footer_y=1190
 p.append(texts(58,footer_y,['Fond moderne : © les contributeurs OpenStreetMap, ODbL 1.0 · extraction du 23 octobre 2026.', 'La carte localise le récit : elle ne restitue pas le bâti, la voirie ni les ponts dans leur état des années 1920.'],15,MUTED,step=24))
 p.append(texts(1540,footer_y,['ENQUÊTE DES 23-24.10.2026', 'Projection locale · coordonnées WGS84'],13,MUTED,step=24,text_anchor='end'))
 p.append('</g></svg>');svg=''.join(p);(OUT/filename).write_text(svg,encoding='utf-8')
 return selected

def interactive(rows,features,b):
 pr,mpp=projector(b,20,20,960,960)
 svg=f'<svg id="atlasMap" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" aria-label="Carte interactive des lieux du roman" role="img"><defs><clipPath id="clip"><rect width="1000" height="1000"/></clipPath></defs><rect width="1000" height="1000" fill="#ece9de"/><g id="world" clip-path="url(#clip)"><g id="base">{base_svg(features,b,pr)}{annotations(b,pr,False)}</g><g id="markers">{map_marks(rows,b,pr,mpp)}</g></g></svg>'
 payload=[]
 for r in rows:
  d=dict(r);a=anchor(d.get('geometry'));d['in_map']=inside(a,b);d['xy']=pr(a) if a else None;payload.append(d)
 json_data=json.dumps(payload,ensure_ascii=False).replace('</','<\\/')
 tmpl='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lyon — Les Deux Étendards · Atlas critique</title><style>
*{box-sizing:border-box}body{margin:0;background:#f7f2e8;color:#243a3f;font-family:Arial,Helvetica,sans-serif}header{padding:30px 4vw 23px;border-bottom:1px solid #d8d2c6}header .eyebrow{text-transform:uppercase;letter-spacing:.17em;font-size:11px;color:#687778}h1{font:40px Georgia,serif;margin:12px 0 9px}header p{margin:0;color:#687778;font-size:14px;line-height:1.5}.layout{display:grid;grid-template-columns:minmax(450px,1fr) 420px;height:calc(100vh - 165px);min-height:650px}.map-panel{position:relative;overflow:hidden;background:#ece9de;display:flex;align-items:center;justify-content:center}#atlasMap{width:100%;height:100%;max-height:calc(100vh - 165px);touch-action:none}.lieu{cursor:pointer;transition:opacity .18s}.lieu:hover,.lieu:focus{filter:drop-shadow(0 0 5px #fff)}.lieu.selected{filter:drop-shadow(0 0 8px #172f38)}.lieu.hidden{display:none}.map-tools{position:absolute;top:18px;left:18px;display:flex;flex-wrap:wrap;max-width:calc(100% - 36px);gap:5px}.map-tools button{border:1px solid #d3cbbd;background:#fffdf8;color:#243a3f;border-radius:6px;padding:9px 13px;font-weight:700;cursor:pointer}.map-caption{position:absolute;left:18px;bottom:18px;right:18px;max-width:620px;background:#fffdf8ec;border:1px solid #d8d2c6;border-radius:7px;padding:12px 15px;font-size:12px;line-height:1.5}.map-caption strong{display:block;font-size:13px}.sidebar{padding:23px 22px;overflow:auto;border-left:1px solid #d8d2c6;background:#fbf8f1}input[type=search]{width:100%;padding:12px;border:1px solid #d4cdbe;border-radius:5px;background:white;color:#243a3f;font-size:14px}.filters{display:flex;flex-wrap:wrap;gap:8px 12px;margin:15px 0;font-size:12px}.filters label{display:flex;align-items:center;gap:4px;cursor:pointer}.count{font-size:12px;color:#687778;margin:13px 0}.entry{width:100%;text-align:left;background:none;border:0;border-top:1px solid #e0dace;padding:12px 0;display:flex;gap:12px;cursor:pointer;color:#243a3f}.entry:hover,.entry.active{background:#efe9dc}.number{font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:0 0 27px;height:27px;border-radius:50%;background:#235460;color:white}.entry.probable .number{background:#b07125;border-radius:4px}.entry.hypothese .number{background:none;color:#b45942;border:1px dashed #b45942}.entry.non_localise .number{background:#7a7772}.entry strong{font-size:14px;display:block;line-height:1.35}.entry small{font-size:11px;color:#687778;display:block;margin-top:4px}.detail{display:none;margin:0 0 18px;padding:16px;background:#efe9dd;border-left:3px solid #235460;border-radius:4px}.detail.open{display:block}.detail h2{font:24px Georgia,serif;margin:0 0 9px}.detail p{font-size:13px;line-height:1.6}.detail .tag{font-size:11px;letter-spacing:.02em;font-weight:700}.detail a{color:#235460;overflow-wrap:anywhere}.detail ul{padding-left:18px;font-size:12px;line-height:1.6}.close{float:right;border:0;background:none;font-size:20px;color:#687778;cursor:pointer}.download{font-size:12px;display:flex;gap:14px;margin-top:16px}.download a,a{color:#235460}.note{font-size:11px;line-height:1.5;color:#687778;margin-top:20px}@media(max-width:850px){header{padding:20px}h1{font-size:30px}.layout{display:block;height:auto}.map-panel{height:65vh;min-height:420px}.sidebar{border-left:0;border-top:1px solid #d8d2c6}.map-caption{font-size:10px;max-width:85%}.map-caption strong{font-size:11px}#atlasMap{max-height:none}}
</style></head><body><header><div class="eyebrow">Lucien Rebatet · Les Deux Étendards · Enquête des 23 et 24 octobre 2026</div><h1>Lyon, une géographie intime</h1><p>Un atlas de lecture : lieux nommés, repères affectifs et identifications à éprouver. Cliquez sur un lieu pour lire sa notice.</p></header><main class="layout"><section class="map-panel">__SVG__<div class="map-tools"><button id="plus" aria-label="Agrandir">+</button><button id="minus" aria-label="Réduire">−</button><button id="reset">Vue d’ensemble</button><button id="focus">Saxe · Guillotière</button></div><div class="map-caption"><strong>Un fond contemporain pour lire un récit des années 1920</strong>© les contributeurs OpenStreetMap · ODbL 1.0 · 23.10.2026.<br>Les cercles/segments translucides signalent une emprise ou une incertitude ; leurs centres ne constituent pas des adresses. Aucune donnée réseau n’est nécessaire.</div></section><aside class="sidebar"><input id="search" type="search" placeholder="Chercher un lieu, une rue…" aria-label="Chercher un lieu"><div class="filters"><label><input type="checkbox" value="atteste" checked>Identifiés</label><label><input type="checkbox" value="probable" checked>Probables</label><label><input type="checkbox" value="hypothese" checked>Hypothèses</label><label><input type="checkbox" value="non_localise" checked>Non localisés</label></div><div id="detail" class="detail" aria-live="polite"></div><p id="count" class="count"></p><div id="entries"></div><div class="download"><a href="lyon_ensemble.svg">Carte générale SVG</a><a href="lyon_guillotiere_saxe.svg">Zoom SVG</a></div><p class="note">Les degrés de certitude portent sur l’identification géographique. La mention dans l’EPUB et la preuve historique sont décrites séparément dans les notices. Un numéro sur une rue ou une zone sert de renvoi, pas de numéro de voirie.</p></aside></main><script type="application/json" id="places">__JSON__</script><script>
'use strict';const places=JSON.parse(document.getElementById('places').textContent);const LABEL={atteste:'Localisation identifiée',probable:'Localisation probable',hypothese:'Hypothèse à vérifier',non_localise:'Non localisé'};const entries=document.getElementById('entries'),detail=document.getElementById('detail'),svg=document.getElementById('atlasMap');let selected=null,view=[0,0,1000,1000];const clean=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const textRef=x=>typeof x==='string'?x:JSON.stringify(x);function safeUrl(s){try{const u=new URL(s,location.href);return ['http:','https:','file:'].includes(u.protocol)?u.href:'#'}catch{return '#'}}
function render(){const q=document.getElementById('search').value.toLocaleLowerCase('fr');const statuses=new Set([...document.querySelectorAll('.filters input:checked')].map(e=>e.value));const shown=places.filter(p=>statuses.has(p.statut)&&(p.nom+' '+p.description+' '+(p.aliases||[]).join(' ')).toLocaleLowerCase('fr').includes(q));const ids=new Set(shown.map(p=>p.id));document.querySelectorAll('.lieu').forEach(el=>el.classList.toggle('hidden',!ids.has(el.dataset.id)));entries.innerHTML=shown.map(p=>`<button class="entry ${p.statut} ${selected===p.id?'active':''}" data-id="${clean(p.id)}"><span class="number">${p.num}</span><span><strong>${clean(p.nom)}</strong><small>${clean(LABEL[p.statut]||p.statut)}${p.in_map?'':' · hors cadre ou sans coordonnées'}</small></span></button>`).join('');document.getElementById('count').textContent=`${shown.length} notice${shown.length>1?'s':''} · ${shown.filter(p=>p.in_map).length} localisation${shown.filter(p=>p.in_map).length>1?'s':''} dans le cadre`;entries.querySelectorAll('button').forEach(e=>e.onclick=()=>select(e.dataset.id));}
function select(id){const p=places.find(p=>p.id===id);if(!p)return;selected=id;document.querySelectorAll('.lieu').forEach(e=>e.classList.toggle('selected',e.dataset.id===id));const refs=(p.refs||[]).map(r=>`<li>${clean(textRef(r))}</li>`).join('');const sources=(p.sources||[]).map(r=>{const u=typeof r==='string'?r:r.url;const title=typeof r==='string'?r:(r.titre||r.title||u);return u?`<li><a href="${clean(safeUrl(u))}" target="_blank" rel="noopener">${clean(title)}</a></li>`:''}).join('');detail.innerHTML=`<button class="close" aria-label="Fermer la notice">×</button><div class="tag">${clean(LABEL[p.statut]||p.statut)} · ${p.num}</div><h2>${clean(p.nom)}</h2><p>${clean(p.description)}</p>${p.precision_m?`<p>Emprise / incertitude indicative : ${clean(p.precision_m)} m.</p>`:''}${refs?'<p><b>Repères dans le témoin EPUB</b></p><ul>'+refs+'</ul>':''}${sources?'<p><b>Sources externes</b></p><ul>'+sources+'</ul>':''}${p.fiche?`<p><a href="${clean('https://github.com/Ludwig-H/Rebatet/blob/main/IdentificationsLieux/Lyon/'+p.fiche.replace('../',''))}" target="_blank" rel="noopener">Fiche détaillée dans le dépôt</a></p>`:''}`;detail.classList.add('open');detail.querySelector('.close').onclick=()=>{detail.classList.remove('open');selected=null;render()};render();}
document.querySelectorAll('.lieu').forEach(e=>{e.addEventListener('click',()=>select(e.dataset.id));e.addEventListener('keydown',k=>{if(k.key==='Enter'||k.key===' '){k.preventDefault();select(e.dataset.id)}})});document.getElementById('search').addEventListener('input',render);document.querySelectorAll('.filters input').forEach(e=>e.addEventListener('change',render));function setView(v){view=v;svg.setAttribute('viewBox',v.join(' '))}function zoom(f){const [x,y,w,h]=view;const nw=Math.max(180,Math.min(1400,w*f));setView([x+(w-nw)/2,y+(h-nw)/2,nw,nw])}document.getElementById('plus').onclick=()=>zoom(.75);document.getElementById('minus').onclick=()=>zoom(1.33);document.getElementById('reset').onclick=()=>setView([0,0,1000,1000]);document.getElementById('focus').onclick=()=>setView([490,330,380,530]);let drag=null;svg.addEventListener('pointerdown',e=>{if(e.target.closest('.lieu'))return;drag={x:e.clientX,y:e.clientY,view:[...view]};svg.setPointerCapture(e.pointerId)});svg.addEventListener('pointermove',e=>{if(!drag)return;const rect=svg.getBoundingClientRect();const s=Math.min(rect.width/view[2],rect.height/view[3]);setView([drag.view[0]-(e.clientX-drag.x)/s,drag.view[1]-(e.clientY-drag.y)/s,drag.view[2],drag.view[3]])});svg.addEventListener('pointerup',()=>drag=null);render();
</script></body></html>'''
 (OUT/'atlas_lyon.html').write_text(tmpl.replace('__SVG__',svg).replace('__JSON__',json_data),encoding='utf-8')

def main():
 OUT.mkdir(exist_ok=True)
 rows=normalise(json.loads((DATA/'lieux.json').read_text(encoding='utf-8')))
 features=json.loads((DATA/'fond_osm.geojson').read_text(encoding='utf-8'))['features']
 general=[4.810,45.740,4.860,45.780];zoom=[4.836,45.7498,4.8530,45.7670]
 a=static_svg(rows,features,general,'Lyon, une géographie intime','Repères du roman et lieux identifiés · centre de Lyon',False,'lyon_ensemble.svg')
 z=static_svg(rows,features,zoom,'De Saxe à la Guillotière','Café des Alpes, rue du Six-Janvier et Place Antique · lecture rapprochée',True,'lyon_guillotiere_saxe.svg')
 interactive(rows,features,general)
 manifest={'generated':'2026-10-24','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs':{f:hashlib.sha256((DATA/f).read_bytes()).hexdigest() for f in ['lieux.json','fond_osm.geojson']},'outputs':{f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in ['lyon_ensemble.svg','lyon_guillotiere_saxe.svg','atlas_lyon.html']},'ensemble_ids':[r['id'] for r in a],'zoom_ids':[r['id'] for r in z],'projection':'Local equirectangular, phi0=45.76 deg, WGS84 input','limits':'Modern OSM base. Editorial static selection: 18 base loci, plus Brazier and Lugdunum in overview. Full dataset appears in HTML.'}
 (OUT/'manifest_cartes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'{len(rows)} notices; cartes statiques {len(a)}/{len(z)} lieux; atlas autonome généré.')
if __name__=='__main__':main()
