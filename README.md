# Germinares Health Dashboard v2

Dashboard automatizado de análise de produtividade e crescimento para 216 Germinares PicPay.

**URL Pública:** https://ti-corp-picpay.github.io/germinares-health-dashboard/

## 🎯 O que o Dashboard Mostra

### **Health Score (0-100)**
Score consolidado baseado em 6 dimensões:
- Entrega (25%)
- Eficiência (20%)
- Consistência (15%)
- Atividade (15%)
- Qualidade (15%)
- WIP (10%)

### **DORA Metrics (GitHub)**
Métricas de engenharia de software:
- **Deployment Frequency** — PRs merged por semana
- **Lead Time** — Tempo de PR aberta → merged (P50/P90)
- **Review Time** — Tempo até primeira review
- **Throughput** — % de PRs merged
- **Batch Size** — Linhas alteradas por PR (P50/P90)
- **Rework Rate** — % de PRs com múltiplos ciclos

### **Evolução & Velocity**
Crescimento individual ao longo do tempo:
- **Velocity Score** — Aceleração/desaceleração (últimas 4 semanas)
- **Skill Evolution Index** — Crescimento de complexidade e autonomia
- **Momentum Score** — Consistência vs intermitência
- **Sparklines** — Throughput visual (últimas 12 semanas)
- **Heatmap** — Consistência semanal (12 semanas)

---

## 📁 Estrutura do Projeto

```
germinares-health-dashboard/
├── .github/
│   └── workflows/
│       └── update-dashboard-v2.yml    # Workflow diário
├── scripts/
│   ├── extract_v2.py                  # Extração Jira + GitHub (DORA)
│   └── generate_html_v2.py            # Geração HTML
├── data/
│   └── germinares-emails.txt          # Lista de emails
├── output/                             # Gerado automaticamente
│   └── index.html                     # Dashboard final
└── README.md
```

---

## 🔧 Como Funciona

### **Extração (extract_v2.py)**

1. **Jira** — Últimas 90 dias de issues
   - Issues assigned/created por germinar
   - Granularidade semanal (últimas 12 semanas)
   - Cycle time, aging, projetos, tipos de issues
   
2. **GitHub** — Últimas 30 dias de PRs
   - PRs abertas/merged por usuário
   - Detalhes de cada PR (lead time, batch size, reviews)
   - Métricas DORA: P50/P90, review time, rework rate

3. **Cálculos** — Health Score + DORA + Evolução
   - 6 dimensões do Health Score
   - Velocity Score (tendência 4 semanas)
   - Skill Evolution (complexidade crescente)
   - Momentum (consistência 12 semanas)

### **Geração (generate_html_v2.py)**

- Renderiza HTML standalone (~110KB)
- Seções: Health, DORA, Evolução, Metodologia
- Sparklines, heatmaps, gráficos temporais
- Navegação com dots, animações, responsivo

### **Deploy (GitHub Actions)**

- Workflow roda diariamente às 09:00 BRT (seg-sex)
- Deploy automático no GitHub Pages (branch `gh-pages`)
- Histórico limpo (force_orphan)

---

## 🚀 Setup

### 1. Configurar Secrets

No repositório, adicionar em **Settings → Secrets → Actions**:

- `JIRA_EMAIL` — Email Atlassian (ex: natali.lee@picpay.com)
- `JIRA_TOKEN` — API Token do Jira ([gerar aqui](https://id.atlassian.com/manage-profile/security/api-tokens))
- `GH_PAT` — GitHub Personal Access Token com `repo` e `read:org` ([gerar aqui](https://github.com/settings/tokens))

### 2. Ativar GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch: **gh-pages** / **/ (root)**

### 3. Executar Workflow

- **Manual:** Actions → Update Germinares Dashboard v2 → Run workflow
- **Automático:** Roda todo dia útil às 09:00 BRT

---

## 📊 Métricas Disponíveis

### **Por Germinar:**
- Health Score (0-100) + 6 dimensões
- Jira: assigned, done, in progress, todo, cycle time, aging, completion rate, projetos
- GitHub: PRs opened/merged, reviews given, lead time, batch size, rework rate, throughput
- Evolução: velocity score, skill evolution, momentum, sparklines, heatmap 12 semanas

### **Agregadas:**
- Distribuição de Health Score (Saudável/Atenção/Risco)
- Alertas críticos (aging, WIP alto, inatividade)
- Métricas DORA médias (deployment freq, lead time P50/P90, throughput)

---

## ⚠️ Limitações Conhecidas

### **Rate Limiting GitHub**
- API GitHub: 5.000 requests/hora (autenticado)
- Script limita a 15 PRs por usuário
- Sleep de 0.3s entre requests
- Tempo total: ~30-40min

### **Dados Aproximados (até primeiro run completo)**
- Enquanto não rodar extract_v2.py, métricas DORA são estimativas
- Lead Time usa cycle time do Jira como proxy
- Batch size e review time são mocks

---

## 🔗 Links Úteis

- **Dashboard:** https://ti-corp-picpay.github.io/germinares-health-dashboard/
- **Repositório:** https://github.com/ti-corp-picpay/germinares-health-dashboard
- **DORA Research:** https://dora.dev/research
- **Jira PicPay:** https://picpay.atlassian.net

---

## 📝 Changelog

### v2.0 (Mar 2026)
- ✅ Adicionadas métricas DORA (Deployment Frequency, Lead Time, Review Time, Throughput, Batch Size, Rework)
- ✅ Adicionadas métricas de Evolução (Velocity Score, Skill Evolution, Momentum)
- ✅ Sparklines de throughput (12 semanas)
- ✅ Heatmap de consistência (12 semanas)
- ✅ Granularidade semanal nos dados Jira
- ✅ Extração detalhada de PRs do GitHub

### v1.0 (Mar 2026)
- ✅ Health Score com 6 dimensões
- ✅ Dados Jira (últimos 30 dias)
- ✅ Dados GitHub básicos (PRs, reviews)
- ✅ Deploy automático GitHub Pages

---

**Mantido por:** Natali Lee (@natali.lee)  
**Última atualização:** 25/03/2026
