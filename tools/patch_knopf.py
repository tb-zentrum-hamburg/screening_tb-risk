#!/usr/bin/env python3
"""Fügt den Knopf 'Daten aktualisieren' (Inzidenz/MDR aus daten.json) in die Seiten ein. Idempotent."""
import re,sys,os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
BAR='<div class="dbar" id="dbar">Datenstand Inzidenz und MDR/RR: <span id="dstand">eingebettete Tabelle (Stand 22.11.2026)</span> <button type="button" id="dbtn">Daten aktualisieren</button></div>'
CSS='<style>.dbar{margin:0 0 12px;font-size:14px;color:#526477}.dbar button{margin:0 0 0 6px}#datDialog{width:min(720px,calc(100% - 28px));max-height:calc(100vh - 40px);border:0;border-radius:14px;padding:0;box-shadow:0 12px 40px #0006;color:#1d2d3e}#datDialog::backdrop{background:rgba(17,31,52,.56)}#datDialog .dd-body{padding:20px 24px}#datDialog h2{margin:0 0 8px;border:0;padding:0;font-size:22px}#datDialog table{border-collapse:collapse;width:100%;font-size:14px;margin:10px 0}#datDialog th,#datDialog td{border-bottom:1px solid #d8dee6;padding:5px 8px;text-align:left}#datDialog tr.chg td{background:#fff3cd;font-weight:600}#datDialog .dd-scroll{max-height:50vh;overflow:auto}#datDialog .dd-act{display:flex;gap:10px;justify-content:flex-end;margin-top:14px}@media print{.dbar,#datDialog{display:none}}</style>'
DLG='<dialog id="datDialog" aria-labelledby="ddTitle"><div class="dd-body"><h2 id="ddTitle">Daten aktualisieren</h2><div id="ddInfo"></div><div class="dd-scroll" id="ddList"></div><div class="dd-act"><button type="button" id="ddOk">Übernehmen</button><button type="button" id="ddCancel">Schließen</button></div></div></dialog>'
JS=r'''<script>(function(){
var U='daten.json',dlg=document.getElementById('datDialog'),info=document.getElementById('ddInfo'),list=document.getElementById('ddList'),ok=document.getElementById('ddOk'),pend=null;
if(!dlg||!dlg.showModal)return;
function e(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function f(a){if(!a)return'–';return (a[0]==null?'–':String(a[0]).replace('.',','))+' / '+(a[1]==null?'–':(a[1]*100).toFixed(1).replace('.',',')+' %')}
function cl(a){return !!a&&((a[0]!=null&&a[0]>100)||(a[1]!=null&&a[1]>0.10))}
function same(a,b){return a&&b&&a[0]===b[0]&&a[1]===b[1]}
function opts(){['country','transit'].forEach(function(id){var s=document.getElementById(id);if(!s)return;var v=s.value,first=s.firstElementChild;while(s.children.length>1)s.removeChild(s.lastChild);Object.keys(data).sort(function(a,b){return a.localeCompare(b,'de')}).forEach(function(c){var o=document.createElement('option');o.value=o.textContent=c;s.appendChild(o)});s.value=v})}
document.getElementById('dbtn').addEventListener('click',function(){
 pend=null;ok.hidden=true;info.textContent='Lade aktuelle Daten …';list.innerHTML='';dlg.showModal();
 fetch(U,{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(j){
  var ch=[],nw=[],k;for(k in j.data){var o=data[k],n=j.data[k];if(!o)nw.push(k);else if(!same(o,n))ch.push(k)}
  var head='Datenstand: '+e(j.stand)+' · Quelle: '+e(j.quelle)+'. Angezeigt: Inzidenz je 100.000 / MDR-Anteil.';
  if(!ch.length&&!nw.length){info.innerHTML=head+'<br><b>Keine Änderungen gegenüber den aktuell verwendeten Werten.</b>';document.getElementById('dstand').textContent=j.quelle+' (Stand '+j.stand+')';return}
  var flips=ch.filter(function(c){return cl(data[c])!==cl(j.data[c])}).length;
  info.innerHTML=head+'<br><b>'+ch.length+' Länder geändert'+(nw.length?', '+nw.length+' neu':'')+'</b>'+(flips?'; <b>bei '+flips+' ändert sich die Einstufung</b> (Röntgen-Kriterium Inzidenz &gt; 100 oder MDR &gt; 10 %).':'.')+' Vor dem Übernehmen bitte prüfen; die Übernahme gilt nur für diese Sitzung, bis die Seite neu geladen wird.';
  var h='<table><tr><th>Land</th><th>bisher</th><th>neu</th><th>Hinweis</th></tr>';
  ch.concat(nw).forEach(function(c){var o=data[c],n=j.data[c],fl=o&&cl(o)!==cl(n);h+='<tr'+(fl?' class="chg"':'')+'><td>'+e(c)+'</td><td>'+f(o)+'</td><td>'+f(n)+'</td><td>'+(!o?'neu':fl?(cl(n)?'jetzt im Röntgen-Screening':'nicht mehr im Röntgen-Screening'):'')+'</td></tr>'});
  list.innerHTML=h+'</table>';pend=j;ok.hidden=false;
 }).catch(function(){info.innerHTML='<b>Abruf nicht möglich.</b> Die Aktualisierung funktioniert nur über die veröffentlichte Seite mit Internetverbindung (nicht bei lokal geöffneter Datei).'});
});
ok.addEventListener('click',function(){if(!pend)return;for(var k in pend.data)data[k]=pend.data[k];opts();document.getElementById('dstand').textContent=pend.quelle+' (Stand '+pend.stand+', aktualisiert)';pend=null;dlg.close();try{render()}catch(x){}});
document.getElementById('ddCancel').addEventListener('click',function(){dlg.close()});
})();</script>'''
def patch(path):
    s=open(path,encoding='utf-8').read()
    if 'id="dbtn"' in s: return False
    assert s.count('<form id="f">')==1,path
    s=s.replace('<form id="f">',BAR+'<form id="f">',1)
    p=s.rstrip().rfind('</html>'); q=s[:p].rstrip().endswith('</body>')
    if q: p=s.rfind('</body>',0,p)
    s=s[:p]+CSS+DLG+JS+s[p:]
    open(path,'w',encoding='utf-8').write(s); return True
if __name__=='__main__':
    for f in ['ifsg36','praxis']:
        print(f,patch(os.path.join(ROOT,f+'.html')))
