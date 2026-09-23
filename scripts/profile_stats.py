import os, json, urllib.request, html, datetime
from pathlib import Path
USER = os.environ["PROFILE_USER"]
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = Path("assets")
def api(url, data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={"Authorization": "Bearer "+TOKEN, "Accept": "application/vnd.github+json", "User-Agent": "profile-assets"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)
def text(x,y,value,size=18,color="#c9d1d9"):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>'
def svg(name,w,h,body):
    OUT.joinpath(name+".svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" rx="12" fill="#11151e"/>{body}</svg>')
repos=[]
for page in range(1,11):
    batch=api(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}")
    repos.extend(r for r in batch if not r["private"] and not r["fork"])
    if len(batch)<100: break
langs={}
for repo in repos:
    for lang,size in api(repo["languages_url"]).items(): langs[lang]=langs.get(lang,0)+size
query="""query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
data=api("https://api.github.com/graphql", {"query":query,"variables":{"login":USER}})
if data.get("errors"): raise RuntimeError(data["errors"])
cal=data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days=[d for w in cal["weeks"] for d in w["contributionDays"]]
today=datetime.date.today().isoformat()
days=[d for d in days if d["date"]<=today]
best=run=0
for d in days:
    run=run+1 if d["contributionCount"] else 0
    best=max(best,run)
current=0
tail=days[:-1] if days and days[-1]["date"]==today and days[-1]["contributionCount"]==0 else days
for d in reversed(tail):
    if not d["contributionCount"]: break
    current+=1
stamp=datetime.date.today().strftime("%d/%m/%Y")
body=text(25,37,"GitHub Stats",24,"#ec4899")
for i,(label,value) in enumerate([("Repositórios públicos próprios",len(repos)),("Estrelas recebidas",sum(r["stargazers_count"] for r in repos)),("Contribuições nos últimos 12 meses",cal["totalContributions"])]):
    body+=text(25,83+i*42,label,16)+text(420,83+i*42,value,23,"#f9a8d4")
body+=text(25,219,"Dados do GitHub · "+stamp,12,"#8b949e")
svg("stats",500,240,body)
body=text(25,37,"Linguagens mais usadas",24,"#ec4899")
total=sum(langs.values()) or 1
for i,(lang,size) in enumerate(sorted(langs.items(),key=lambda x:x[1],reverse=True)[:5]):
    y=70+i*29
    body+=text(25,y,lang,15)+f'<rect x="150" y="{y-12}" width="{max(2,230*size/total)}" height="10" rx="5" fill="#db2777"/>'+text(400,y,f"{size/total:.1%}",14)
body+=text(25,228,"Proporção de bytes · repositórios públicos próprios",11,"#8b949e")
svg("languages",500,240,body)
body=text(25,37,"Consistência",24,"#ec4899")
for x,value,label in [(25,current,"dias na sequência atual"),(365,best,"melhor sequência (12 meses)"),(705,sum(d["contributionCount"]>0 for d in days),"dias ativos (12 meses)")]:
    body+=text(x,91,value,38,"#f9a8d4")+text(x,125,label,15)
body+=text(25,162,"Sequência atual considera hoje ou ontem como último dia ativo.",12,"#8b949e")
svg("streak",1000,185,body)
recent=days[-30:]
peak=max([d["contributionCount"] for d in recent]+[1])
points=" ".join(f"{35+i*930/max(1,len(recent)-1):.1f},{195-d['contributionCount']/peak*125:.1f}" for i,d in enumerate(recent))
body=text(25,38,"Atividade · últimos 30 dias",24,"#ec4899")
body+='<path d="M35 195H965" stroke="#30363d"/><polyline points="'+points+'" fill="none" stroke="#ec4899" stroke-width="3"/>'
body+=text(35,225,recent[0]["date"],12,"#8b949e")+text(850,225,recent[-1]["date"],12,"#8b949e")
body+=text(25,258,str(sum(d["contributionCount"] for d in recent))+" contribuições no período",14,"#f9a8d4")
svg("activity",1000,280,body)
