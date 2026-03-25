#!/usr/bin/env python3
"""
Germinares Health Dashboard - Extraction & Generation
Extrai dados do Jira e GitHub, calcula Health Score e gera dashboard HTML
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import base64

# Config
JIRA_BASE = "https://picpay.atlassian.net"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not JIRA_EMAIL or not JIRA_TOKEN:
    print("ERROR: JIRA_EMAIL and JIRA_TOKEN required")
    sys.exit(1)

JIRA_AUTH = (JIRA_EMAIL, JIRA_TOKEN)
GH_HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"} if GITHUB_TOKEN else None

print("=== GERMINARES HEALTH DASHBOARD EXTRACTION ===")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

# Load emails
with open('data/germinares-emails.txt', 'r', encoding='utf-8') as f:
    emails = [line.strip() for line in f if '@' in line]
print(f"Germinares: {len(emails)}")

# === JIRA EXTRACTION ===
print("\n=== JIRA EXTRACTION ===")
BATCH_SIZE = 15
all_issues = {}
batch_num = 0

for i in range(0, len(emails), BATCH_SIZE):
    batch_num += 1
    batch = emails[i:i+BATCH_SIZE]
    email_list = ",".join([f"'{e}'" for e in batch])
    
    for query_type in ['assignee', 'reporter']:
        field = 'updated' if query_type == 'assignee' else 'created'
        jql = f"{query_type} IN ({email_list}) AND {field} >= -30d"
        
        page_token = None
        while True:
            body = {
                "jql": jql,
                "maxResults": 100,
                "fields": ["key","summary","status","assignee","project","created","updated","resolutiondate","issuetype","priority","reporter"]
            }
            if page_token:
                body["nextPageToken"] = page_token
            
            try:
                resp = requests.post(f"{JIRA_BASE}/rest/api/3/search/jql", json=body, auth=JIRA_AUTH, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                
                for issue in data.get("issues", []):
                    if issue["key"] not in all_issues:
                        all_issues[issue["key"]] = issue
                
                if data.get("isLast", True):
                    break
                page_token = data.get("nextPageToken")
            except Exception as e:
                print(f"  Batch {batch_num} {query_type}: ERROR - {e}")
                break
    
    print(f"  Batch {batch_num}: {len(all_issues)} issues total")

print(f"\nTotal issues: {len(all_issues)}")

# Process Jira data
now = datetime.now()
summary_by_user = {email: {
    'assigned_total': 0, 'assigned_done': 0, 'assigned_in_progress': 0, 'assigned_todo': 0,
    'created_total': 0, 'cycle_times': [], 'aging_values': [], 'projects': set(), 'weekly_activity': [0,0,0,0]
} for email in emails}

issues_list = []
for key, issue in all_issues.items():
    f = issue['fields']
    status = f['status']['name'].lower()
    
    if any(x in status for x in ['done','resolved','closed','complete','finaliz','conclu']):
        status_cat = 'done'
    elif any(x in status for x in ['progress','review','test','qa','dev','waiting','analysis']):
        status_cat = 'in_progress'
    else:
        status_cat = 'todo'
    
    created = datetime.fromisoformat(f['created'].replace('Z', '+00:00'))
    updated = datetime.fromisoformat(f['updated'].replace('Z', '+00:00'))
    resolved = datetime.fromisoformat(f['resolutiondate'].replace('Z', '+00:00')) if f.get('resolutiondate') else None
    
    cycle_time = (resolved - created).days if resolved else None
    aging = (now - created.replace(tzinfo=None)).days if not resolved else None
    
    assignee_email = f.get('assignee', {}).get('emailAddress') if f.get('assignee') else None
    reporter_email = f.get('reporter', {}).get('emailAddress') if f.get('reporter') else None
    
    issues_list.append({
        'key': key, 'status_category': status_cat, 'cycle_time_days': cycle_time,
        'aging_days': aging, 'assignee_email': assignee_email, 'reporter_email': reporter_email,
        'project': f['project']['key'], 'updated': f['updated']
    })
    
    # Update summary
    if assignee_email and assignee_email in summary_by_user:
        s = summary_by_user[assignee_email]
        s['assigned_total'] += 1
        s[f'assigned_{status_cat}'] += 1
        s['projects'].add(f['project']['key'])
        if cycle_time: s['cycle_times'].append(cycle_time)
        if aging: s['aging_values'].append(aging)
        
        # Weekly activity
        days_ago = (now - updated.replace(tzinfo=None)).days
        if days_ago <= 7: s['weekly_activity'][3] += 1
        elif days_ago <= 14: s['weekly_activity'][2] += 1
        elif days_ago <= 21: s['weekly_activity'][1] += 1
        elif days_ago <= 30: s['weekly_activity'][0] += 1
    
    if reporter_email and reporter_email in summary_by_user:
        summary_by_user[reporter_email]['created_total'] += 1

# === GITHUB EXTRACTION ===
print("\n=== GITHUB EXTRACTION ===")
github_summary = {}
email_to_github = {}

if GITHUB_TOKEN:
    org_members_resp = requests.get("https://api.github.com/orgs/PicPay/members?per_page=100", headers=GH_HEADERS, timeout=30)
    all_members = []
    page = 1
    while True:
        resp = requests.get(f"https://api.github.com/orgs/PicPay/members?per_page=100&page={page}", headers=GH_HEADERS, timeout=30)
        if resp.status_code != 200 or not resp.json():
            break
        all_members.extend([m['login'] for m in resp.json()])
        page += 1
        if len(resp.json()) < 100:
            break
    
    member_set = {m.lower(): m for m in all_members}
    print(f"Org members: {len(member_set)}")
    
    # Map emails to GitHub users
    for email in emails:
        prefix = email.split('@')[0]
        variations = [
            prefix.replace('.', '-'),
            prefix.replace('.', ''),
            prefix
        ]
        for v in variations:
            if v.lower() in member_set:
                email_to_github[email] = member_set[v.lower()]
                break
    
    print(f"Mapped: {len(email_to_github)}/{len(emails)}")
    
    # Extract PRs (with rate limiting)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    for email, gh_user in email_to_github.items():
        try:
            # Search PRs
            pr_url = f"https://api.github.com/search/issues?q=type:pr+author:{gh_user}+org:PicPay+created:>{thirty_days_ago}&per_page=100"
            pr_resp = requests.get(pr_url, headers=GH_HEADERS, timeout=30)
            prs = pr_resp.json().get('items', []) if pr_resp.status_code == 200 else []
            
            merged = [p for p in prs if p.get('pull_request', {}).get('merged_at')]
            
            # Search reviews
            rv_url = f"https://api.github.com/search/issues?q=type:pr+reviewed-by:{gh_user}+org:PicPay+created:>{thirty_days_ago}&per_page=1"
            rv_resp = requests.get(rv_url, headers=GH_HEADERS, timeout=30)
            reviews = rv_resp.json().get('total_count', 0) if rv_resp.status_code == 200 else 0
            
            github_summary[email] = {
                'github_username': gh_user,
                'prs_opened': len(prs),
                'prs_merged': len(merged),
                'reviews_given': reviews
            }
        except:
            pass
    
    print(f"GitHub data extracted: {len(github_summary)} users")
else:
    print("GITHUB_TOKEN not set - skipping GitHub extraction")

# === CALCULATE HEALTH SCORES ===
print("\n=== CALCULATING HEALTH SCORES ===")
germinares = []

for email in emails:
    j = summary_by_user[email]
    g = github_summary.get(email, {})
    
    jd = j['assigned_done']
    jt = j['assigned_total']
    ji = j['assigned_in_progress']
    jo = j['assigned_todo']
    jcy = sum(j['cycle_times']) / len(j['cycle_times']) if j['cycle_times'] else 0
    ja = max(j['aging_values']) if j['aging_values'] else 0
    jcomp = round(jd / jt * 100, 1) if jt > 0 else 0
    
    gp = g.get('prs_opened', 0)
    gm = g.get('prs_merged', 0)
    gr = g.get('reviews_given', 0)
    gu = g.get('github_username')
    
    # Dimensions
    d1_entrega = min(100, (jd * 2 + gm * 3) * 2)
    d2_efic = 100 if jcy <= 3 else 80 if jcy <= 7 else 60 if jcy <= 14 else 40 if jcy <= 21 else 20 if jcy > 0 else 0
    d3_consist = sum(1 for w in j['weekly_activity'] if w > 0) / 4 * 100
    
    # Last activity
    last_updated = max([datetime.fromisoformat(i['updated'].replace('Z', '+00:00')) for i in issues_list if i['assignee_email'] == email], default=None)
    days_since = (now - last_updated.replace(tzinfo=None)).days if last_updated else 30
    d4_ativ = 100 if days_since <= 1 else 85 if days_since <= 3 else 65 if days_since <= 7 else 40 if days_since <= 14 else max(0, 100 - days_since * 3)
    
    qual_comp = jcomp
    qual_age = 100 if ja <= 7 else 75 if ja <= 14 else 50 if ja <= 21 else 25
    d5_qual = round(qual_comp * 0.6 + qual_age * 0.4)
    
    d6_wip = 100 if 1 <= ji <= 3 else 70 if 4 <= ji <= 5 else max(10, 100 - (ji - 3) * 15) if ji > 5 else 80 if jd > 0 else 0
    
    health_score = round(d1_entrega * 0.25 + d2_efic * 0.20 + d3_consist * 0.15 + d4_ativ * 0.15 + d5_qual * 0.15 + d6_wip * 0.10, 1)
    health_score = max(0, min(100, health_score))
    
    health_class = 'saudavel' if health_score >= 80 else 'atencao' if health_score >= 60 else 'risco'
    
    # Alerts
    alerts = []
    if days_since >= 30 or (jt == 0 and gp == 0): alerts.append('Inativo no periodo')
    elif days_since > 7 and jt > 0: alerts.append(f'Sem atividade ha {round(days_since)}d')
    if ji > 5: alerts.append(f'WIP alto ({ji} simultaneas)')
    if ja > 21: alerts.append(f'Issue parada ha {round(ja)}d')
    if jo > jd and jt > 5: alerts.append('Backlog > entregas')
    if jcomp > 80 and jd > 10: alerts.append('Top performer')
    if gr > 5: alerts.append(f'Reviewer ativo ({gr} reviews)')
    
    germinares.append({
        'e': email, 'n': email.split('@')[0], 'gu': gu, 'hs': health_score, 'hc': health_class,
        'd1': round(d1_entrega), 'd2': d2_efic, 'd3': round(d3_consist), 'd4': round(d4_ativ), 'd5': d5_qual, 'd6': d6_wip,
        'jt': jt, 'jd': jd, 'ji': ji, 'jo': jo, 'jc': jcomp, 'jcy': round(jcy, 1), 'ja': round(ja, 1),
        'jp': list(j['projects']), 'gp': gp, 'gm': gm, 'gr': gr, 'gl': 0,
        'dsa': round(days_since, 1), 'wk': j['weekly_activity'], 'aw': sum(1 for w in j['weekly_activity'] if w > 0),
        'al': alerts
    })

# Sort by score
germinares.sort(key=lambda x: x['hs'], reverse=True)
for i, g in enumerate(germinares):
    g['r'] = i + 1

print(f"Health scores calculated: {len(germinares)}")
print(f"  Saudavel: {sum(1 for g in germinares if g['hc'] == 'saudavel')}")
print(f"  Atencao: {sum(1 for g in germinares if g['hc'] == 'atencao')}")
print(f"  Risco: {sum(1 for g in germinares if g['hc'] == 'risco')}")

# Projects
proj_count = defaultdict(int)
for issue in issues_list:
    proj_count[issue['project']] += 1
projects = [{'n': k, 'c': v} for k, v in sorted(proj_count.items(), key=lambda x: x[1], reverse=True)]

# === GENERATE HTML ===
print("\n=== GENERATING HTML ===")

# Read template
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace data placeholders
data_js = f"const G={json.dumps(germinares)};\nconst P={json.dumps(projects)};"

# Find and replace <script> section
script_start = html.find('<script>')
script_end = html.find('</script>') + 9
before = html[:script_start]
after = html[script_end:]

# Read app.js
with open('scripts/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_html = before + f'<script>\n{data_js}\n{app_js}\n</script>' + after

# Update timestamp in HTML
new_html = new_html.replace('{{UPDATE_DATE}}', datetime.now().strftime('%d/%m/%Y %H:%M'))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✅ Dashboard updated: {len(new_html)} chars")
print(f"   Issues: {len(issues_list)}")
print(f"   Germinares: {len(germinares)}")
print(f"   Projects: {len(projects)}")
