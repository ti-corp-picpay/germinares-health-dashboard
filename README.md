# Germinares Health Dashboard

Dashboard de análise de produtividade dos Germinares PicPay baseado em dados do Jira e GitHub.

## 📊 [Acessar Dashboard](https://ti-corp-picpay.github.io/germinares-health-dashboard/)

**Link público** — acessa de qualquer lugar, sem VPN.

## O que é

Análise quantitativa de 216 Germinares (estagiários/trainees) nos últimos 30 dias:
- **2.592 issues** do Jira
- **178 PRs** do GitHub (39 mapeados)
- **Health Score 0-100** por indivíduo

## Health Score

Cada Germinar recebe 0-100 pontos baseado em:
- 📦 Entrega (25%) — issues done + PRs merged
- ⚡ Eficiência (20%) — cycle time em dias
- 📅 Consistência (15%) — semanas ativas
- 🔥 Atividade (15%) — dias desde última ação
- ✅ Qualidade (15%) — completion rate + aging
- 📊 WIP (10%) — carga simultânea

## Classificação

- 🟢 **Saudável** (80-100 pts) — 11 germinares
- 🟡 **Atenção** (60-79 pts) — 47 germinares
- 🔴 **Risco** (<60 pts) — 158 germinares (inclui 41 inativos)

## Importante

⚠️ **Health Score reflete atividade no período, não competência.**

Um score baixo pode significar:
- Onboarding recente
- Férias ou afastamento
- Realocação de área
- Tarefas em outro sistema
- Falta de visibilidade no Jira/GitHub

**Objetivo:** identificar onde o programa precisa de apoio, não pressionar indivíduos.

---

*Última atualização: 25/03/2026 10:11 · Gerado por Wolf 🐺*