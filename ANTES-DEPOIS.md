# Dashboard v2 — Antes vs Depois

## 🔴 ANTES (Dashboard Atual)

### Seção "Evolução & Velocity"
```
┌──────────────────────────────────────┐
│ Top 20 em Crescimento                │
├──────────────────────────────────────┤
│ 1. mayla.renze                       │
│    V: 85  E: 72  M: 90              │
│    32 done, 1 WIP, 82% comp          │
│    Projetos: INFR                    │
├──────────────────────────────────────┤
│ 2. pedro.snascimento                 │
│    V: 90  E: 68  M: 95              │
│    32 done, 0 WIP, 100% comp         │
│    Projetos: PROMO                   │
└──────────────────────────────────────┘
```

**Problema:** Números sem contexto temporal!
- V: 85 significa o quê? Está acelerando ou desacelerando?
- Sem gráficos, sem evolução ao longo do tempo
- Não mostra SE a pessoa está crescendo

---

## 🟢 DEPOIS (Com extract_v2.py rodando)

### Seção "Evolução & Velocity" — COM DADOS TEMPORAIS

```
┌───────────────────────────────────────────────────────────────┐
│ Top 20 em Crescimento                                         │
├───────────────────────────────────────────────────────────────┤
│ 1. mayla.renze                                   GitHub: mayla│
│    Velocity: 92  Evolution: 88  Momentum: 95                 │
├───────────────────────────────────────────────────────────────┤
│    📊 Throughput (últimas 12 semanas):                       │
│    ▁▂▃▄▅▆▇█▇█▇█  🚀 Acelerando (+2.1 issues/semana)         │
├───────────────────────────────────────────────────────────────┤
│    🗓️ Consistência (12 semanas):                             │
│    🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢  12/12 semanas ativas        │
├───────────────────────────────────────────────────────────────┤
│    📈 Milestones:                                             │
│    ━━●━━━━●━━━━●━━━━●━━━━━►                                 │
│      1ª PR  1º Bug  1ª Story  Reviewer                       │
│      (7d)   (14d)   (28d)     (45d)                          │
├───────────────────────────────────────────────────────────────┤
│    💡 Destaques:                                              │
│    • Cycle time reduziu 60% (12d → 5d)                       │
│    • PR size reduziu 40% (850 → 280 linhas)                  │
│    • 18 reviews dadas (top 5 da turma)                       │
│    • 100% das PRs merged na primeira tentativa               │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 2. pedro.snascimento                        GitHub: pedro-sn  │
│    Velocity: 88  Evolution: 75  Momentum: 100                │
├───────────────────────────────────────────────────────────────┤
│    📊 Throughput (últimas 12 semanas):                       │
│    ▄▄▅▄▄▅▄▅▅▆▆▆  ➡️ Estável (±0.2 issues/semana)            │
├───────────────────────────────────────────────────────────────┤
│    🗓️ Consistência (12 semanas):                             │
│    🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢  12/12 semanas ativas        │
├───────────────────────────────────────────────────────────────┤
│    📈 Milestones:                                             │
│    ━━●━━━━●━━━━●━━━━━━━►                                     │
│      1ª PR  1º Bug  1ª Story                                 │
│      (5d)   (12d)   (21d)                                    │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 16. lucas.taxiotti                      GitHub: LucasTaxiotti│
│    Velocity: 42  Evolution: 58  Momentum: 35                 │
├───────────────────────────────────────────────────────────────┤
│    📊 Throughput (últimas 12 semanas):                       │
│    █▇▆▅▄▃▂▁▁▁▂▂  📉 Desacelerando (-1.8 issues/semana)      │
├───────────────────────────────────────────────────────────────┤
│    🗓️ Consistência (12 semanas):                             │
│    🟢🟢⚪⚪🟢🟢⚪🟢🟢🟢🟢⚪  8/12 semanas ativas (gaps!)   │
├───────────────────────────────────────────────────────────────┤
│    ⚠️ ALERTAS:                                                │
│    • Velocity caindo há 3 semanas consecutivas               │
│    • Gap de 2 semanas sem commits (Jan 15-29)                │
│    • WIP alto (6 issues simultâneas)                         │
│    • Backlog acumulando (18 TODO vs 5 done no mês)           │
├───────────────────────────────────────────────────────────────┤
│    🎯 Ações Recomendadas:                                     │
│    1. Check-in 1:1 urgente — investigar causas               │
│    2. Revisar scope das tarefas atuais (muito complexas?)    │
│    3. Pair programming com mentor esta semana                │
│    4. Reduzir WIP — focar em finalizar vs iniciar            │
└───────────────────────────────────────────────────────────────┘
```

---

## 📊 Visualizações Temporais

### **Sparkline de Throughput**
- **▁▂▃▄▅▆▇█** — Mostra tendência visual das últimas 12 semanas
- Cada barra = issues concluídas naquela semana
- Identifica padrões: crescimento constante, platô, queda

### **Heatmap de Consistência**
- **🟢🟢🟢⚪🟢** — 12 quadrados representando 12 semanas
- 🟢 = semana ativa (≥3 issues)
- ⚪ = semana inativa (0-2 issues)
- Detecta gaps prolongados (alerta vermelho!)

### **Timeline de Milestones**
- Linha do tempo desde entrada no programa
- Marca: 1ª PR, 1º Bug, 1ª Story, 1º Epic, virar reviewer ativo
- Mostra velocidade de evolução (rápido <30d, lento >90d)

### **Gráfico de Destaques**
- Cycle time: comparação primeiro mês vs último mês
- PR size: evolução de batch size (aprendendo a quebrar tarefas)
- Reviews dadas: nível de colaboração
- Rework rate: qualidade/aprendizado

---

## 🎯 Métricas com Significado Real

### **Velocity Score Agora:**
```
Velocity: 92/100 🚀 Acelerando

Semanas:  W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12
Issues:   2   3   3   5   4   7   8   9   10  12  11  13
          ▁   ▂   ▂   ▃   ▃   ▄   ▅   ▆   ▇   █   ▇   █

Trend: +0.9 issues/semana (regressão linear)
Interpretação: Produtividade crescendo consistentemente
```

### **Momentum Score Agora:**
```
Momentum: 35/100 ⚠️ Intermitente

🗓️ Últimas 12 semanas:
🟢🟢⚪⚪🟢🟢⚪🟢🟢🟢🟢⚪

Semanas ativas: 8/12 (67%)
Gap máximo: 2 semanas consecutivas
Interpretação: Padrão irregular — investigar causas dos gaps
```

### **Skill Evolution Agora:**
```
Evolution: 88/100 ⭐ Evoluindo Rápido

━━●━━━━━●━━━━━●━━━━━━●━━━━━━━━━━●━━━►
  Set     Out     Nov      Dez        Jan
  Task    Bug     Story    Epic       Reviewer
  (7d)    (14d)   (28d)    (56d)      (90d)

Complexidade: Task → Story → Epic (crescente)
Autonomia: 60% das issues criadas por ele mesmo
Projetos: 1 → 3 (scope crescente)
Cycle time: 12d → 5d (eficiência +58%)
```

---

## 🔥 Diferença BRUTAL

**ANTES:** "Lucas tem velocity 42" ❓ (E daí?)

**DEPOIS:** "Lucas está desacelerando há 3 semanas (█▇▆▅▄▃▂▁), teve 2 gaps sem commits, WIP subiu de 2 pra 6, e completion rate caiu de 78% pra 52% no último mês. Check-in 1:1 urgente!" 🚨

---

## ⏱️ Quanto Tempo até Ver Isso?

1. **Configurar secrets:** ~3 minutos
2. **Rodar workflow manualmente:** ~35-40 minutos
3. **Dashboard publicado:** Imediato após workflow concluir

**Total:** ~45 minutos até dashboard v2 com dados temporais estar no ar! 🚀

---

**Próximo passo:** Configure os 3 secrets e rode o workflow!

URL dos secrets: https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/secrets/actions
