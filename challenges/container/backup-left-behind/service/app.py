import io, os, tempfile, zipfile
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
FLAG = os.environ.get('FLAG','VARE{backups_belong_outside_webroot}')
def prepare(root):
    root=Path(root); backup=root/'maintenance-backups';backup.mkdir(parents=True,exist_ok=True)
    (root/'index.html').write_text("""<!doctype html><html><head><title>STMU Lab Portal</title></head>
    <body><h1>Teaching lab portal</h1><p>System status: online.</p>
    <p>The site follows the standard robots exclusion convention for crawler instructions.</p>
    <p>Only synthetic classroom data is hosted here.</p></body></html>""",encoding='utf-8')
    (root/'robots.txt').write_text('User-agent: *\nDisallow: /maintenance-backups/\n',encoding='utf-8')
    with zipfile.ZipFile(backup/'portal-backup.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('portal/.env','APP_NAME=TeachingPortal\nAPP_MODE=training\nASSESSMENT_TOKEN='+FLAG+'\n')
        z.writestr('portal/README.txt','Internal deployment backup. This configuration is not intended for unauthenticated website visitors.\n')
        z.writestr('portal/status.csv','asset,state\nlab-vm-01,ready\nlab-vm-02,maintenance\n')
class Handler(SimpleHTTPRequestHandler):
    server_version='STMU-LabPortal/1.0';sys_version=''
if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='vare-web-') as tmp:
        prepare(tmp)
        ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),partial(Handler,directory=tmp)).serve_forever()
