#!/usr/bin/env python3
"""Aktualisiert daten.json (Inzidenz je 100.000 und MDR/RR-Anteil unter neuen Fällen) aus den WHO-TB-Daten.
Quelle: https://extranet.who.int/tme/generateCSV.asp?ds=estimates (Spalten e_inc_100k, e_rr_pct_new, year, iso2).
Länder ohne WHO-Wert behalten den bisherigen Wert. Fixwerte (tools/pins.json) werden nie überschrieben."""
import csv, io, json, sys, urllib.request, datetime, os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
URL='https://extranet.who.int/tme/generateCSV.asp?ds=estimates'
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None
def rnd_inc(v): return round(v,1) if v<10 else int(round(v))
def main(src=None):
    raw=open(src,encoding='utf-8-sig').read() if src else urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=120).read().decode('utf-8-sig')
    rows=list(csv.DictReader(io.StringIO(raw)))
    need={'iso2','year','e_inc_100k'}
    if not rows or not need<=set(rows[0]): sys.exit('WHO-CSV unerwartet aufgebaut: '+str(list(rows[0])[:12] if rows else 'leer'))
    has_mdr='e_rr_pct_new' in rows[0]
    latest={}
    for r in rows:
        y=num(r['year']); 
        if y is None or not r['iso2']: continue
        if r['iso2'] not in latest or y>latest[r['iso2']][0]: latest[r['iso2']]=(y,r)
    lm=json.load(open(os.path.join(ROOT,'tools/laender.json'),encoding='utf-8'))
    pins=json.load(open(os.path.join(ROOT,'tools/pins.json'),encoding='utf-8'))
    cur=json.load(open(os.path.join(ROOT,'daten.json'),encoding='utf-8'))
    data=cur['data']; years=set(); n_upd=0
    for name,iso in lm.items():
        if iso not in latest: continue
        y,r=latest[iso]; years.add(int(y))
        inc=num(r['e_inc_100k']); old=data.get(name,[None,None])
        new_inc=rnd_inc(inc) if inc is not None else old[0]
        mdr=num(r.get('e_rr_pct_new')) if has_mdr else None
        new_mdr=round(mdr/100,3) if mdr is not None else old[1]
        p=pins.get(name,{})
        if 'inc' in p: new_inc=p['inc']
        if 'mdr' in p: new_mdr=p['mdr']
        if [new_inc,new_mdr]!=old: n_upd+=1
        data[name]=[new_inc,new_mdr]
    jahr=max(years) if years else cur.get('jahr')
    out={"stand":datetime.date.today().strftime('%d.%m.%Y'),"quelle":"WHO Global TB Programme, Schätzungen"+(f" {jahr}" if jahr else ""),"jahr":jahr,"data":data}
    if not has_mdr: print('Hinweis: Spalte e_rr_pct_new fehlt, MDR-Werte unverändert')
    json.dump(out,open(os.path.join(ROOT,'daten.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print(f'{n_upd} Länder geändert, Datenjahr {jahr}')
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else None)
