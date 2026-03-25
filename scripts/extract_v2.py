#!/usr/bin/env python3
"""
Germinares Health Dashboard v2 - Extraction & Generation
Extrai Jira + GitHub (com DORA + Evolução), calcula Health Score e gera dashboard HTML
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import time
import statistics

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

print("=== GERMINARES HEALTH DASHBOARD v2 EXTRACTION ===")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

# Load emails
try:
    with open('data/germinares-emails.txt', 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if '@' in line]
except:
    print("ERROR: data/germinares-emails.txt not found")
    sys.exit(1)

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
        jql = f"{query_type} IN ({email_list}) AND {field} >= -90d"
        
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

# Process Jira data (últimas 12 semanas pra evolução)
now = datetime.now()
summary_by_user = {email: {
    'assigned_total': 0, 'assigned_done': 0, 'assigned_in_progress': 0, 'assigned_todo': 0,
    'created_total': 0, 'cycle_times': [], 'aging_values': [], 'projects': set(), 
    'weekly_activity': [0]*12,  # 12 semanas
    'weekly_done': [0]*12,      # Issues concluídas por semana
    'issue_types': [],           # Histórico de tipos
    'self_created_count': 0,     # Issues que ele mesmo criou
    'first_issue_date': None,    # Data da primeira issue
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
    issue_type = f.get('issuetype', {}).get('name', 'Task')
    
    issues_list.append({
        'key': key, 'status_category': status_cat, 'cycle_time_days': cycle_time,
        'aging_days': aging, 'assignee_email': assignee_email, 'reporter_email': reporter_email,
        'project': f['project']['key'], 'updated': f['updated'], 'created': f['created'],
        'resolved': f.get('resolutiondate'), 'type': issue_type
    })
    
    # Update summary
    if assignee_email and assignee_email in summary_by_user:
        s = summary_by_user[assignee_email]
        s['assigned_total'] += 1
        s[f'assigned_{status_cat}'] += 1
        s['projects'].add(f['project']['key'])
        s['issue_types'].append(issue_type)
        if cycle_time: s['cycle_times'].append(cycle_time)
        if aging: s['aging_values'].append(aging)
        
        # Primeira issue
        if not s['first_issue_date'] or created < datetime.fromisoformat(s['first_issue_date'].replace('Z', '+00:00')):
            s['first_issue_date'] = f['created']
        
        # Weekly activity (últimas 12 semanas)
        weeks_ago = (now - updated.replace(tzinfo=None)).days // 7
        if weeks_ago < 12:
            s['weekly_activity'][11 - weeks_ago] += 1
        
        # Weekly done (últimas 12 semanas)
        if status_cat == 'done' and resolved:
            weeks_ago_done = (now - resolved.replace(tzinfo=None)).days // 7
            if weeks_ago_done < 12:
                s['weekly_done'][11 - weeks_ago_done] += 1
    
    if reporter_email and reporter_email in summary_by_user:
        summary_by_user[reporter_email]['created_total'] += 1
        if assignee_email == reporter_email:
            summary_by_user[reporter_email]['self_created_count'] += 1

# === GITHUB EXTRACTION (ENRICHED) ===
print("\n=== GITHUB EXTRACTION (ENRICHED WITH DORA) ===")
github_summary = {}
email_to_github = {}

if GITHUB_TOKEN:
    # Map emails to GitHub users (reuso lógica existente)
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
    
    # Extract PRs with DORA metrics
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    user_count = 0
    
    for email, gh_user in email_to_github.items():
        user_count += 1
        print(f"  [{user_count}/{len(email_to_github)}] {gh_user}...", end=" ")
        
        try:
            # Search PRs
            pr_search_url = f"https://api.github.com/search/issues?q=type:pr+author:{gh_user}+org:PicPay+created:>{thirty_days_ago}&per_page=100&sort=created&order=desc"
            pr_resp = requests.get(pr_search_url, headers=GH_HEADERS, timeout=30)
            
            if pr_resp.status_code == 403:
                print("Rate limited - waiting 60s...")
                time.sleep(60)
                pr_resp = requests.get(pr_search_url, headers=GH_HEADERS, timeout=30)
            
            if pr_resp.status_code != 200:
                print(f"Error {pr_resp.status_code}")
                continue
            
            prs = pr_resp.json().get('items', [])
            
            # Extract detailed metrics
            lead_times = []
            review_times = []
            batch_sizes = []
            rework_count = 0
            merged_count = 0
            
            for pr in prs[:15]:  # Limitar a 15 PRs pra não estourar rate limit
                try:
                    pr_url = pr['pull_request']['url']
                    pr_detail_resp = requests.get(pr_url, headers=GH_HEADERS, timeout=30)
                    
                    if pr_detail_resp.status_code != 200:
                        continue
                    
                    pr_detail = pr_detail_resp.json()
                    
                    created_at = datetime.fromisoformat(pr_detail['created_at'].replace('Z', '+00:00'))
                    merged_at = datetime.fromisoformat(pr_detail['merged_at'].replace('Z', '+00:00')) if pr_detail.get('merged_at') else None
                    
                    # Lead Time
                    if merged_at:
                        lead_time_hours = (merged_at - created_at).total_seconds() / 3600
                        lead_times.append(lead_time_hours)
                        merged_count += 1
                    
                    # Batch Size
                    additions = pr_detail.get('additions', 0)
                    deletions = pr_detail.get('deletions', 0)
                    batch_sizes.append(additions + deletions)
                    
                    # Reviews
                    reviews_url = f"{pr_url}/reviews"
                    reviews_resp = requests.get(reviews_url, headers=GH_HEADERS, timeout=30)
                    if reviews_resp.status_code == 200:
                        reviews = reviews_resp.json()
                        if reviews:
                            first_review_at = datetime.fromisoformat(reviews[0]['submitted_at'].replace('Z', '+00:00'))
                            review_time_hours = (first_review_at - created_at).total_seconds() / 3600
                            review_times.append(review_time_hours)
                            
                            # Rework detection
                            if len(reviews) > 2:
                                rework_count += 1
                    
                    time.sleep(0.3)  # Rate limiting
                
                except Exception as e:
                    continue
            
            # Search reviews given
            rv_url = f"https://api.github.com/search/issues?q=type:pr+reviewed-by:{gh_user}+org:PicPay+created:>{thirty_days_ago}&per_page=1"
            rv_resp = requests.get(rv_url, headers=GH_HEADERS, timeout=30)
            reviews_given = rv_resp.json().get('total_count', 0) if rv_resp.status_code == 200 else 0
            
            # Calculate aggregated metrics
            github_summary[email] = {
                'github_username': gh_user,
                'total_prs': len(prs),
                'merged_prs': merged_count,
                'open_prs': len([p for p in prs if p['state'] == 'open']),
                'reviews_given': reviews_given,
                
                # DORA Metrics
                'deploy_freq_week': round(merged_count / 4.3, 2),
                'lead_time_avg': round(statistics.mean(lead_times), 1) if lead_times else 0,
                'lead_time_p50': round(statistics.median(lead_times), 1) if lead_times else 0,
                'lead_time_p90': round(statistics.quantiles(lead_times, n=10)[8], 1) if len(lead_times) >= 10 else (max(lead_times) if lead_times else 0),
                'review_time_avg': round(statistics.mean(review_times), 1) if review_times else 0,
                'review_time_p50': round(statistics.median(review_times), 1) if review_times else 0,
                'batch_size_avg': round(statistics.mean(batch_sizes), 0) if batch_sizes else 0,
                'batch_size_p50': round(statistics.median(batch_sizes), 0) if batch_sizes else 0,
                'batch_size_p90': round(statistics.quantiles(batch_sizes, n=10)[8], 0) if len(batch_sizes) >= 10 else (max(batch_sizes) if batch_sizes else 0),
                'rework_rate': round(rework_count / len(prs) * 100, 1) if prs else 0,
                'throughput': round(merged_count / len(prs) * 100, 1) if prs else 0,
            }
            
            print(f"OK ({len(prs)} PRs, {merged_count} merged)")
        
        except Exception as e:
            print(f"Error: {e}")
            github_summary[email] = {'error': str(e)}
    
    print(f"\nGitHub data extracted: {len(github_summary)} users")
else:
    print("GITHUB_TOKEN not set - skipping GitHub extraction")

# === CALCULATE METRICS (Health + Evolution + Velocity) ===
print("\n=== CALCULATING METRICS ===")
germinares = []

for email in emails:
    j = summary_by_user[email]
    g = github_summary.get(email, {})
    
    # Jira basics
    jd = j['assigned_done']
    jt = j['assigned_total']
    ji = j['assigned_in_progress']
    jo = j['assigned_todo']
    jcy = statistics.mean(j['cycle_times']) if j['cycle_times'] else 0
    ja = max(j['aging_values']) if j['aging_values'] else 0
    jcomp = round(jd / jt * 100, 1) if jt > 0 else 0
    
    # GitHub basics
    gp = g.get('total_prs', 0)
    gm = g.get('merged_prs', 0)
    gr = g.get('reviews_given', 0)
    gu = g.get('github_username')
    
    # === VELOCITY SCORE ===
    # Últimas 4 semanas de issues concluídas
    last_4_weeks = j['weekly_done'][-4:]
    if sum(last_4_weeks) > 0:
        # Trend linear simples
        trend = (last_4_weeks[-1] - last_4_weeks[0]) / 3 if len([w for w in last_4_weeks if w > 0]) >= 2 else 0
        velocity_score = max(0, min(100, 50 + (trend * 20)))
    else:
        velocity_score = 0
    
    # === SKILL EVOLUTION INDEX ===
    # Complexidade crescente (tipos de issues)
    unique_types = len(set(j['issue_types']))
    has_story = 'Story' in j['issue_types']
    has_epic = 'Epic' in j['issue_types']
    complexity_score = (unique_types * 20) + (30 if has_story else 0) + (30 if has_epic else 0)
    
    # Autonomia (% self-created)
    autonomy_score = (j['self_created_count'] / jt * 100) if jt > 0 else 0
    
    # Eficiência (cycle time melhorando - simplificado)
    efficiency_score = 100 if jcy <= 7 else 70 if jcy <= 14 else 40
    
    # Escopo (projetos)
    scope_score = min(100, len(j['projects']) * 33)
    
    skill_evolution = round(
        complexity_score * 0.4 +
        autonomy_score * 0.25 +
        efficiency_score * 0.2 +
        scope_score * 0.15,
        1
    )
    
    # === MOMENTUM SCORE ===
    active_weeks = sum(1 for w in j['weekly_activity'][-8:] if w > 0)
    # Detectar gap máximo
    max_gap = 0
    current_gap = 0
    for w in j['weekly_activity'][-8:]:
        if w == 0:
            current_gap += 1
            max_gap = max(max_gap, current_gap)
        else:
            current_gap = 0
    
    consistency = active_weeks / 8 * 100
    gap_penalty = max_gap * 10
    momentum_score = max(0, consistency - gap_penalty)
    
    # === HEALTH SCORE (original) ===
    d1_entrega = min(100, (jd * 2 + gm * 3) * 2)
    d2_efic = 100 if jcy <= 3 else 80 if jcy <= 7 else 60 if jcy <= 14 else 40 if jcy <= 21 else 20 if jcy > 0 else 0
    d3_consist = sum(1 for w in j['weekly_activity'][-4:] if w > 0) / 4 * 100
    
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
    if velocity_score < 40: alerts.append('Velocity em queda')
    if momentum_score < 50: alerts.append('Momentum baixo')
    if jcomp > 80 and jd > 10: alerts.append('Top performer')
    if gr > 5: alerts.append(f'Reviewer ativo ({gr} reviews)')
    
    germinares.append({
        'e': email, 'n': email.split('@')[0], 'gu': gu, 'hs': health_score, 'hc': health_class,
        'd1': round(d1_entrega), 'd2': d2_efic, 'd3': round(d3_consist), 'd4': round(d4_ativ), 'd5': d5_qual, 'd6': d6_wip,
        'jt': jt, 'jd': jd, 'ji': ji, 'jo': jo, 'jc': jcomp, 'jcy': round(jcy, 1), 'ja': round(ja, 1),
        'jp': list(j['projects']), 'gp': gp, 'gm': gm, 'gr': gr,
        'dsa': round(days_since, 1), 'wk': j['weekly_activity'][-4:], 'wk12': j['weekly_activity'],
        'wd': j['weekly_done'][-4:], 'wd12': j['weekly_done'],
        'vs': round(velocity_score, 1), 'se': round(skill_evolution, 1), 'ms': round(momentum_score, 1),
        'al': alerts,
        # DORA
        'df': g.get('deploy_freq_week', 0),
        'lt_p50': g.get('lead_time_p50', 0),
        'lt_p90': g.get('lead_time_p90', 0),
        'rt_p50': g.get('review_time_p50', 0),
        'bs_p50': g.get('batch_size_p50', 0),
        'bs_p90': g.get('batch_size_p90', 0),
        'rw': g.get('rework_rate', 0),
        'tp': g.get('throughput', 0),
    })

# Sort by health score
germinares.sort(key=lambda x: x['hs'], reverse=True)
for i, g in enumerate(germinares):
    g['r'] = i + 1

print(f"Metrics calculated: {len(germinares)}")
print(f"  Saudavel: {sum(1 for g in germinares if g['hc'] == 'saudavel')}")
print(f"  Atencao: {sum(1 for g in germinares if g['hc'] == 'atencao')}")
print(f"  Risco: {sum(1 for g in germinares if g['hc'] == 'risco')}")

# Save data
with open('dashboard_data_v2.json', 'w', encoding='utf-8') as f:
    json.dump({
        'extraction_date': datetime.now().isoformat(),
        'total_germinares': len(emails),
        'germinares': germinares,
        'jira_issues': len(all_issues),
        'github_users_mapped': len(email_to_github),
    }, f, indent=2, ensure_ascii=False)

print(f"\nData saved to dashboard_data_v2.json")
print("\n=== EXTRACTION COMPLETE ===")
print("Next: Generate dashboard HTML with generate_dashboard_v2.py")
