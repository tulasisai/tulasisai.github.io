"""Build the GitHub Pages portfolio from the resume data (single source of truth).

    python build_site.py      -> writes index.html, <role>/index.html, resumes/*.pdf
"""
import html
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "resumes"))
from build_resumes import CERTIFICATIONS, CONTACT, EDUCATION, ROLES, OUT as RESUME_OUT  # noqa: E402

SLUGS = {
    "System_Administrator": ("sysadmin", "Systems Administration"),
    "Network_Engineer": ("network", "Network Engineering"),
    "IT_Technician": ("it-support", "IT Support"),
    "Python_Developer": ("python", "Python Development"),
}

ALL_PROJECTS = []
for r in ROLES.values():
    for p in r["projects"]:
        if p not in ALL_PROJECTS:
            ALL_PROJECTS.append(p)

e = html.escape


def page(title, desc, body, depth):
    root = "../" * depth
    nav = "".join(
        f'<a href="{root}{slug}/">{e(label)}</a>' for slug, label in SLUGS.values()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="{root}">Tulasisai Pechetti</a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <a href="mailto:{e(CONTACT['email'])}">{e(CONTACT['email'])}</a> ·
  <a href="{e(CONTACT['linkedin'])}">LinkedIn</a> ·
  <a href="{e(CONTACT['github'])}">GitHub</a>
</footer>
</body>
</html>
"""


def project_cards(projects):
    out = []
    for name, tech, bullets in projects:
        items = "".join(f"<li>{e(b)}</li>" for b in bullets)
        chips = "".join(f"<span>{e(t.strip())}</span>" for t in tech.split(","))
        out.append(f'<article class="card"><h3>{e(name)}</h3><div class="chips">{chips}</div><ul>{items}</ul></article>')
    return "\n".join(out)


def role_page(key, role):
    slug, label = SLUGS[key]
    pdf = f"../resumes/Tulasisai_Pechetti_{key}.pdf"
    skills = "".join(
        f"<div class='skill'><h4>{e(l)}</h4><p>{e(v)}</p></div>" for l, v in role["skills"]
    )
    exp = []
    for (title, org, dates), bullets in role["experience"]:
        items = "".join(f"<li>{e(b)}</li>" for b in bullets)
        exp.append(
            f"<article class='job'><div class='job-head'><h3>{e(title)}</h3><span>{e(dates)}</span></div>"
            f"<p class='org'>{e(org)}</p><ul>{items}</ul></article>"
        )
    edu = "".join(f"<li><strong>{e(d)}</strong>, {e(s)} ({e(t)})</li>" for d, s, t in EDUCATION)
    certs = "".join(f"<li>{e(c)}</li>" for c in CERTIFICATIONS)
    body = f"""
<section class="hero">
  <p class="eyebrow">{e(label)}</p>
  <h1>{e(role['title'])}</h1>
  <p class="lead">{e(role['summary'])}</p>
  <div class="cta">
    <a class="btn" href="{pdf}" download>Download résumé (PDF)</a>
    <a class="btn ghost" href="mailto:{e(CONTACT['email'])}">Contact me</a>
  </div>
</section>
<section><h2>Skills</h2><div class="skills">{skills}</div></section>
<section><h2>Experience</h2>{''.join(exp)}</section>
<section><h2>Projects</h2><div class="grid">{project_cards(role['projects'])}</div></section>
<section><h2>Certifications</h2><ul class="edu">{certs}</ul></section>
<section><h2>Education</h2><ul class="edu">{edu}</ul></section>
"""
    return page(f"{role['title']} · Tulasisai Pechetti", role["summary"], body, 1)


def index_page():
    cards = []
    for key, role in ROLES.items():
        slug, label = SLUGS[key]
        cards.append(
            f'<a class="card role" href="{slug}/"><p class="eyebrow">{e(label)}</p>'
            f'<h3>{e(role["title"])}</h3><p>{e(role["summary"].split(". ")[0])}.</p><span class="more">View profile →</span></a>'
        )
    body = f"""
<section class="hero">
  <p class="eyebrow">IT · Networking · Systems · Python</p>
  <h1>Tulasisai Pechetti</h1>
  <p class="lead">IT and software engineer supporting 200+ users and 190+ Windows endpoints. Hands-on with Microsoft 365,
  Intune, Entra ID, enterprise networking and Python automation. M.S. in Computer and Information Sciences, University of North Texas.</p>
  <div class="cta">
    <a class="btn" href="mailto:{e(CONTACT['email'])}">Get in touch</a>
    <a class="btn ghost" href="{e(CONTACT['linkedin'])}">LinkedIn</a>
  </div>
</section>
<section><h2>Choose a focus</h2><div class="grid">{''.join(cards)}</div></section>
<section><h2>Projects</h2><div class="grid">{project_cards(ALL_PROJECTS)}</div></section>
"""
    return page("Tulasisai Pechetti · Portfolio", "IT, networking, systems administration and Python portfolio.", body, 0)


CSS = """
:root{--bg:#f7f8fa;--surface:#fff;--text:#18212f;--muted:#5a6678;--accent:#1f5fae;--border:#e3e7ee;--chip:#eef3fa}
@media (prefers-color-scheme:dark){:root{--bg:#0f141b;--surface:#161d27;--text:#e6ebf2;--muted:#9aa7b8;--accent:#6aa8ff;--border:#253041;--chip:#1c2735}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.top{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;padding:16px max(16px,calc((100% - 1040px)/2));border-bottom:1px solid var(--border);background:var(--surface);position:sticky;top:0;z-index:1}
.brand{font-weight:700;color:var(--text)}
nav{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:.95rem}
main{max-width:1040px;margin:0 auto;padding:0 16px;overflow-wrap:anywhere}
section{padding:40px 0;border-bottom:1px solid var(--border)}
section:last-child{border:0}
.hero{padding:64px 0 48px}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;font-weight:600;color:var(--accent);margin:0 0 8px}
h1{font-size:clamp(2rem,5vw,3rem);line-height:1.1;margin:0 0 16px}
h2{font-size:1.4rem;margin:0 0 20px}
h3{margin:0 0 6px;font-size:1.08rem}
.lead{font-size:1.12rem;color:var(--muted);max-width:720px;margin:0}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.btn{display:inline-block;padding:10px 18px;border-radius:8px;background:var(--accent);color:#fff;font-weight:600}
.btn:hover{text-decoration:none;opacity:.9}
.btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px;color:var(--text)}
.card ul{padding-left:18px;margin:10px 0 0;color:var(--muted);font-size:.95rem}
.card.role{display:flex;flex-direction:column;transition:border-color .15s}
.card.role:hover{border-color:var(--accent);text-decoration:none}
.card.role p{color:var(--muted);margin:0 0 12px;font-size:.95rem}
.more{margin-top:auto;color:var(--accent);font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips span{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:.8rem;color:var(--muted)}
.skills{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:12px}
.skill{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.skill h4{margin:0 0 4px;font-size:.95rem}.skill p{margin:0;color:var(--muted);font-size:.92rem}
.job{margin-bottom:28px}
.job-head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 16px;align-items:baseline}
.job-head span,.org{color:var(--muted);font-size:.92rem}
.org{margin:0 0 6px;font-style:italic}
.job ul{margin:0;padding-left:20px}
.edu{padding-left:20px}
footer{text-align:center;padding:32px 16px;color:var(--muted);font-size:.9rem;border-top:1px solid var(--border)}
"""

if __name__ == "__main__":
    (HERE / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (HERE / "index.html").write_text(index_page(), encoding="utf-8")
    res = HERE / "resumes"
    res.mkdir(exist_ok=True)
    for key, role in ROLES.items():
        slug, _ = SLUGS[key]
        d = HERE / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(role_page(key, role), encoding="utf-8")
        pdf = RESUME_OUT / f"Tulasisai_Pechetti_{key}.pdf"
        if pdf.exists():
            shutil.copy2(pdf, res / pdf.name)
    (HERE / ".nojekyll").touch()
    print("site built in", HERE)
