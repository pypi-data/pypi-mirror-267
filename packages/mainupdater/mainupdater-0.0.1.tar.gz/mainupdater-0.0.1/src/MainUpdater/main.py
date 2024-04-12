import os,requests
import MainShortcuts as ms
from traceback import print_exc
try:
  import progressbar
  bar=True
except:
  bar=False
pbar_w=[
  progressbar.Percentage(),
  progressbar.GranularBar(
    left="(",
    right=")",
    ),
  progressbar.ETA(
    format="%(eta)8s",
    format_finished="%(elapsed)8s",
    format_na="     N/A",
    format_not_started="--:--:--",
    format_zero="00:00:00",
    ),
  ]
def get_pbar(size=progressbar.UnknownLength):
  pbar=progressbar.ProgressBar(
    widgets=pbar_w,
    max_error=False,
    min_value=0,
    max_value=size,
    )
  return None
def _request(method,url,**kw):
  if not "headers" in kw:kw["headers"]={}
  if "data" in kw:
    if type(kw["data"]) in [dict,list,tuple,type(True),type(False),type(None)]:
      kw["data"]=ms.json.encode(kw["data"])
      kw["headers"]["Content-Type"]="application/json"
  r=requests.request(method,url,**kw)
  r.raise_for_status()
  return r
def get_info(url,**kw):
  kw["stream"]=False
  r=_request("GET",url,**kw)
  info=r.json()
  r.close()
  if info["info"]["url"]!=url:
    kw={}
    if "request" in info["info"]:
      kw=info["info"]["request"]
    info=get_info(info["info"]["url"],**kw)
  return info
def download_url(url,path,cli=False,**kw):
  print("Downloading a file")
  kw["stream"]=True
  r=_request("GET",url,**kw)
  if cli:
    if "Content-Length" in r.headers:
      pbar=get_pbar(int(r.headers["Content-Length"]))
    else:
      pbar=get_pbar()
  with open(path,"wb") as f:
    c=0
    if cli:pbar.start()
    for i in r.iter_content(1024):
      if i:
        f.write(i)
        c+=len(i)
        if cli:
          pbar.term_width=os.get_terminal_size()[0]-1
          pbar.update(i)
  r.close()
  if cli:pbar.finish()
  return c
def update(path,info_old,cli=False):
  if cli:
    print('Updating file "{}"'.format(path))
    print("Getting information about a file")
  kw={}
  if "request" in info_old["info"]:
    kw=info["info"]["request"]
  info_new=get_info(info_old["info"]["url"],**kw)
  kw={}
  if "request" in info["file"]:
    kw=info["file"]["request"]
  if ms.path.exists(path):
    if info_new["info"]["version"]>info_old["info"]["version"]:
      download_url(info_new["file"]["url"],path,cli=cli,**kw)
  else:
    download_url(info_new["file"]["url"],path,cli=cli,**kw)
  return info_new
def update_all(path,cli=False):
  if os.path.isdir(path):
    for i in os.listdir(path):
      if os.path.isfile(f"{path}/{i}"):
        if i.lower().endswith(".mainupdater"):
          update_all(f"{path}/{i}",cli=cli)
  elif os.path.isfile(path):
    info=ms.json.read(path)
    for k,v in info["files"].items():
      try:
        info["files"][k]=update(k,v,cli=cli)
      except:
        print_exc()
    ms.json.write(path,info)
    