import json, os, re, io, warnings, zipfile
warnings.filterwarnings("ignore"); import logging; logging.disable(logging.CRITICAL)
from pypdf import PdfReader
ROOT='/home/manishmehta/ui-projects/ibis-industries'
z=zipfile.ZipFile('/home/manishmehta/ui-projects/business-stuff/IBISReports-20260807T194014Z-1-001.zip')
items=json.load(open(f'{ROOT}/_run300.json')); done=0
for it in items:
    if os.path.exists(it['file']) and os.path.getsize(it['file'])>2000: done+=1; continue
    try:
        r=PdfReader(io.BytesIO(z.read(it['zippath'])))
        txt=[]
        for pg in r.pages[:22]:
            try: txt.append(pg.extract_text() or "")
            except: pass
        full="\n".join(txt)
        full=re.sub(r'\n?\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [AP]M [^\n]*','',full)
        full=re.sub(r'https://www\.searchfunder\.com/\S+','',full)
        full=re.sub(r'\n{3,}','\n\n',full).strip()
        open(it['file'],'w').write(full[:38000]); done+=1
        if done%25==0: print("extracted",done,"/",len(items),flush=True)
    except Exception as e: print("FAIL",it['slug'],str(e)[:70],flush=True)
print("ALL DONE",done,"/",len(items))
