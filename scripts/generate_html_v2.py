#!/usr/bin/env python3
"""
Dashboard HTML Generator v2
Gera dashboard com DORA + Evolução usando dados temporais (12 semanas)
"""
import json
import sys
from datetime import datetime

print("=== DASHBOARD HTML GENERATOR V2 ===")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

# Carregar dados
try:
    with open('dashboard_data_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("ERRO: dashboard_data_v2.json não encontrado!")
    print("Execute extract_v2.py primeiro.")
    sys.exit(1)

germinares = data['germinares']
extraction_date = datetime.fromisoformat(data['extraction_date']).strftime('%d/%m/%Y %H:%M BRT')

print(f"Germinares carregados: {len(germinares)}")

# Calcular métricas agregadas DORA
all_deploy_freq = [g['df'] for g in germinares if g['df'] > 0]
all_lead_time = [g['lt_p50'] for g in germinares if g['lt_p50'] > 0]
all_throughput = [g['tp'] for g in germinares if g['tp'] > 0]
all_batch_size = [g['bs_p50'] for g in germinares if g['bs_p50'] > 0]

dora_agg = {
    'deploy_freq': round(sum(all_deploy_freq) / len(all_deploy_freq), 1) if all_deploy_freq else 0,
    'lead_time_p50': round(sum(all_lead_time) / len(all_lead_time), 1) if all_lead_time else 0,
    'throughput': round(sum(all_throughput) / len(all_throughput), 0) if all_throughput else 0,
    'batch_size': round(sum(all_batch_size) / len(all_batch_size), 0) if all_batch_size else 0,
}

print(f"Métricas DORA agregadas calculadas")

# Função: gerar sparkline
def sparkline(values):
    """Gera sparkline ASCII de uma lista de valores."""
    if not values or max(values) == 0:
        return '▁' * len(values)
    bars = '▁▂▃▄▅▆▇█'
    max_val = max(values)
    return ''.join(bars[min(7, int(v / max_val * 7))] for v in values)

# Função: classificar benchmark
def classify_benchmark(metric, value):
    """Classifica métrica em Elite/High/Medium/Low."""
    thresholds = {
        'deploy_freq': [(3, 'Elite'), (1, 'High'), (0.5, 'Medium')],
        'lead_time': [(4, 'Elite'), (12, 'High'), (48, 'Medium')],
        'throughput': [(90, 'Elite'), (75, 'High'), (50, 'Medium')],
        'velocity': [(80, 'Elite'), (60, 'High'), (40, 'Medium')],
    }
    
    for thresh, level in thresholds.get(metric, []):
        if metric in ['throughput', 'velocity', 'deploy_freq']:
            if value >= thresh:
                return level
        else:
            if value < thresh:
                return level
    return 'Low'

# HTML base
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Germinares Health Dashboard v2 - PicPay</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0A0E1A;--bg2:#111827;--card:rgba(255,255,255,0.05);--cb:rgba(255,255,255,0.08);--tx:#F0F0F5;--mu:#8B8FA3;--gr:#21C25E;--yl:#F5A623;--rd:#EF4444;--bl:#3B82F6;--cy:#06B6D4}}
html{{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx);line-height:1.6}}
.c{{max-width:1360px;margin:0 auto;padding:0 20px}}
section{{padding:80px 0 40px}}
.sl{{font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gr);margin-bottom:6px;padding-left:14px;position:relative}}
.sl::before{{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);width:3px;height:14px;background:var(--gr);border-radius:2px}}
.st{{font-size:clamp(24px,3.5vw,36px);font-weight:800;margin-bottom:6px;line-height:1.15}}
.sd{{color:var(--mu);font-size:13px;max-width:560px;margin-bottom:32px}}
.cd{{background:var(--card);border:1px solid var(--cb);border-radius:14px;padding:20px;transition:.3s}}
.cd:hover{{border-color:rgba(255,255,255,0.12)}}
.kg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-bottom:28px}}
.kv{{font-size:clamp(32px,4vw,48px);font-weight:900}}
.kl{{font-size:11px;color:var(--mu);font-weight:500;margin-top:2px}}
.hs-badge{{display:inline-block;padding:3px 10px;border-radius:10px;font-size:10px;font-weight:700;margin-top:8px}}
.hs-sau{{background:rgba(33,194,94,0.2);color:#86efac}}
.hs-ate{{background:rgba(245,166,35,0.2);color:#fcd34d}}
.hs-ris{{background:rgba(239,68,68,0.2);color:#fca5a5}}
.info-box{{background:rgba(103,232,249,0.05);border-left:4px solid #67e8f9;padding:20px;border-radius:8px;margin-bottom:24px}}
.info-box h3{{font-size:14px;font-weight:700;color:#67e8f9;margin-bottom:8px}}
.info-box p{{font-size:12px;color:var(--mu);line-height:1.6}}
.evolution-card{{background:rgba(255,255,255,0.03);border:1px solid var(--cb);border-radius:12px;padding:18px;margin-bottom:14px}}
.evolution-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px}}
.evolution-name{{font-size:16px;font-weight:700}}
.score-badges{{display:flex;gap:8px;flex-wrap:wrap}}
.score-badge{{padding:4px 10px;border-radius:8px;font-size:11px;font-weight:700}}
.sparkline{{font-family:monospace;letter-spacing:-1px;font-size:16px}}
.heatmap{{display:flex;gap:4px;margin:8px 0}}
.hm-week{{width:24px;height:24px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700}}
.hm-active{{background:rgba(33,194,94,0.3);color:var(--gr)}}
.hm-inactive{{background:rgba(255,255,255,0.03);color:var(--mu)}}
</style>
</head>
<body>
<div class="c">

<h1 class="st" style="margin-top:40px">Germinares Health Dashboard v2</h1>
<p class="sd">Produtividade, DORA Metrics e Evolucao Individual | Atualizado em {extraction_date}</p>

<!-- DORA Section -->
<section id="dora">
<div class="sl" style="color:#67e8f9">DORA Metrics</div>
<h2 class="st">Metricas de Engenharia - GitHub</h2>
<div class="sd">Framework DORA + Flow Metrics (ultimos 30 dias)</div>

<div class="info-box">
<h3>🎯 O que sao metricas DORA?</h3>
<p>
<strong style="color:var(--tx)">DORA (DevOps Research and Assessment)</strong> e um framework de pesquisa do Google 
que identifica 4 metricas-chave que diferenciam times de alta performance: <strong>Deployment Frequency</strong>, 
<strong>Lead Time</strong>, <strong>Change Failure Rate</strong> e <strong>Time to Restore</strong>. 
Complementamos com metricas de flow (Review Time, Batch Size, Throughput).
</p>
</div>

<div class="kg">
<div class="cd">
<div class="kl">DEPLOYMENT FREQUENCY</div>
<div class="kv" style="color:var(--gr)">{dora_agg['deploy_freq']}</div>
<div class="kl">PRs merged / semana</div>
<span class="hs-badge hs-sau">High Performer</span>
</div>

<div class="cd">
<div class="kl">LEAD TIME (P50)</div>
<div class="kv" style="color:var(--bl)">{dora_agg['lead_time_p50']:.1f}h</div>
<div class="kl">PR aberta → merged</div>
<span class="hs-badge hs-sau">Elite Performer</span>
</div>

<div class="cd">
<div class="kl">THROUGHPUT</div>
<div class="kv" style="color:var(--gr)">{dora_agg['throughput']}%</div>
<div class="kl">PRs merged / PRs abertas</div>
<span class="hs-badge hs-sau">High Performer</span>
</div>

<div class="cd">
<div class="kl">BATCH SIZE (P50)</div>
<div class="kv" style="color:var(--yl)">{dora_agg['batch_size']}</div>
<div class="kl">linhas alteradas / PR</div>
<span class="hs-badge hs-ate">Saudavel</span>
</div>
</div>

</section>

<!-- Evolução Section -->
<section id="evolution">
<div class="sl" style="color:var(--gr)">Evolucao & Velocity</div>
<h2 class="st">Crescimento Individual</h2>
<div class="sd">Como cada Germinar esta evoluindo ao longo do tempo</div>

<div class="info-box" style="border-color:var(--gr);background:rgba(33,194,94,0.05)">
<h3 style="color:var(--gr)">📈 Metricas de Crescimento</h3>
<p>
<strong style="color:var(--tx)">Velocity Score:</strong> Tendencia de aceleracao/desaceleracao (ultimas 4 semanas). 
<strong style="color:var(--tx)">Skill Evolution:</strong> Crescimento de complexidade e autonomia. 
<strong style="color:var(--tx)">Momentum:</strong> Consistencia vs intermitencia. 
Graficos e heatmaps mostram a evolucao semana a semana.
</p>
</div>

<h3 style="font-size:20px;font-weight:700;margin-bottom:20px">Top 20 em Crescimento</h3>

"""

# Gerar cards de evolução com dados temporais
top20_evolution = sorted(
    [g for g in germinares if g['jt'] > 5],
    key=lambda x: x['vs'],
    reverse=True
)[:20]

for i, g in enumerate(top20_evolution):
    # Status label
    if g['vs'] >= 80:
        status_emoji, status_text = '🚀', 'Acelerando'
    elif g['vs'] >= 60:
        status_emoji, status_text = '📈', 'Crescendo'
    elif g['vs'] >= 40:
        status_emoji, status_text = '➡️', 'Estavel'
    else:
        status_emoji, status_text = '📉', 'Desacelerando'
    
    # Sparkline das últimas 12 semanas (weekly_done)
    spark = sparkline(g['wd12'])
    
    # Heatmap de consistência (weekly_activity)
    heatmap_html = ''.join([
        f'<div class="hm-week hm-{"active" if w >= 3 else "inactive"}">{w if w > 0 else ""}</div>'
        for w in g['wk12']
    ])
    
    # GitHub link
    github_link = f'<a href="https://github.com/{g["gu"]}" target="_blank" style="color:#67e8f9;text-decoration:none;font-size:11px">{g["gu"]}</a>' if g.get('gu') else ''
    
    html += f"""
<div class="evolution-card">
<div class="evolution-header">
<div class="evolution-name">{i+1}. {g['n']}</div>
<div class="score-badges">
<span class="score-badge" style="background:rgba(33,194,94,0.15);color:var(--gr)">V: {g['vs']}</span>
<span class="score-badge" style="background:rgba(59,130,246,0.15);color:var(--bl)">E: {g['se']}</span>
<span class="score-badge" style="background:rgba(6,182,212,0.15);color:var(--cy)">M: {g['ms']}</span>
</div>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:12px">
<div>
<div style="font-size:11px;color:var(--mu);margin-bottom:4px">Throughput (12 semanas):</div>
<div class="sparkline" style="color:var(--gr)">{spark}</div>
</div>
<div>
<div style="font-size:11px;color:var(--mu);margin-bottom:4px">Status:</div>
<div style="font-size:14px;font-weight:600">{status_emoji} {status_text}</div>
</div>
<div>
<div style="font-size:11px;color:var(--mu);margin-bottom:4px">Metricas Jira:</div>
<div style="font-size:12px">{g['jd']} done · {g['ji']} WIP · {round(g['jc'])}%</div>
</div>
</div>

<div style="margin-bottom:12px">
<div style="font-size:11px;color:var(--mu);margin-bottom:6px">Consistencia (ultimas 12 semanas):</div>
<div class="heatmap">{heatmap_html}</div>
<div style="font-size:9px;color:var(--mu);margin-top:4px">
🟢 = ≥3 issues/semana · Semanas ativas: {g['aw']}/12
</div>
</div>

<div style="font-size:10px;color:var(--mu)">
Projetos: {', '.join(g['jp'][:5])}{'...' if len(g['jp']) > 5 else ''} | {github_link}
</div>

</div>
"""

html += """
</section>

<footer style="text-align:center;color:var(--mu);font-size:11px;padding:40px 0;border-top:1px solid var(--cb)">
Dashboard v2 com DORA + Evolucao | Dados: Jira + GitHub | Germinares PicPay 2025
</footer>

</div>
</body>
</html>
"""

# Salvar
output_dir = 'output'
import os
os.makedirs(output_dir, exist_ok=True)

output_file = f'{output_dir}/index.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n=== DASHBOARD HTML GENERATED ===")
print(f"Output: {output_file}")
print(f"Size: {len(html) / 1024:.1f} KB")
print(f"Sections: DORA + Evolution with temporal data (12 weeks)")
