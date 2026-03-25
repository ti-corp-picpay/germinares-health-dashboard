# ✅ Checklist — Dashboard v2 Completo

## 📦 Status Atual

✅ Repositório criado e configurado  
✅ Scripts de extração v2 prontos (DORA + Evolução com 12 semanas)  
✅ Gerador HTML v2 pronto (sparklines, heatmaps, timelines)  
✅ Workflow GitHub Actions configurado  
✅ Documentação completa (README, SETUP-SECRETS, ANTES-DEPOIS)  
✅ Push realizado pro repositório  

---

## 🔐 Próximos Passos (SEU TURNO!)

### 1. Configurar Secrets (3 minutos)

Acesse: https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/secrets/actions

Adicionar 3 secrets:

- [ ] **JIRA_EMAIL** → Seu email Atlassian (natali.lee@picpay.com)
- [ ] **JIRA_TOKEN** → Gerar em https://id.atlassian.com/manage-profile/security/api-tokens
- [ ] **GH_PAT** → Gerar em https://github.com/settings/tokens (scopes: `repo` + `read:org`)

### 2. Rodar Workflow Manualmente (primeira vez)

Acesse: https://github.com/ti-corp-picpay/germinares-health-dashboard/actions

- [ ] Clicar em "Update Germinares Dashboard v2"
- [ ] Clicar em "Run workflow" (botão direita superior)
- [ ] Selecionar branch "master"
- [ ] Clicar em "Run workflow" (botão verde)
- [ ] Aguardar ~35-40 minutos (acompanhar logs)

### 3. Ativar GitHub Pages

Acesse: https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/pages

- [ ] Source: **Deploy from a branch**
- [ ] Branch: **gh-pages** / **/ (root)**
- [ ] Clicar em "Save"
- [ ] Aguardar ~2min
- [ ] Acessar: https://ti-corp-picpay.github.io/germinares-health-dashboard/

---

## 🎯 O que Você Vai Ver (Após Workflow Completar)

### **Dashboard Completo com:**

✅ **Health Score Original** (tudo que já existia)
- KPIs gerais
- Distribuição Saudável/Atenção/Risco
- Alertas acionáveis
- Ranking individual completo
- Ficha detalhada (modal)

✅ **DORA & Flow Metrics** (NOVO!)
- Deployment Frequency
- Lead Time P50/P90 REAL (dados GitHub)
- Review Time P50 REAL
- Throughput (PRs merged/abertas)
- Batch Size P50/P90 (linhas/PR)
- Rework Rate (% multi-review)
- Top 10 ranking por Lead Time
- Benchmarks Elite/High/Medium/Low

✅ **Evolução & Velocity** (NOVO!)
- Top 20 em crescimento
- Velocity Score (tendência 4 semanas)
- Skill Evolution Index (complexidade crescente)
- Momentum Score (consistência 12 semanas)
- **Sparklines** de throughput (12 semanas) ← VISUAL!
- **Heatmap** de consistência (12 semanas) ← VISUAL!
- **Timeline** de milestones ← TEMPORAL!
- Alertas de evolução (desaceleração, gaps, estagnação)
- Destaques individuais (cycle time, PR size, reviews)

---

## ⏱️ Timeline Esperada

| Momento | Ação | Tempo |
|---------|------|-------|
| **Agora** | Você configura secrets | 3 min |
| **+3min** | Você roda workflow manual | 1 clique |
| **+38min** | Workflow completa extração | 35-40 min |
| **+40min** | Dashboard v2 publicado no GitHub Pages | Automático |
| **Total** | Dashboard v2 no ar com dados temporais | ~43 min |

---

## 🐛 Se Algo Der Errado

### Workflow falha no step "Extract Jira + GitHub Data"

**Possíveis causas:**
- Secrets não configurados → Verificar nomes EXATOS (JIRA_EMAIL, JIRA_TOKEN, GH_PAT)
- Token Jira expirado → Gerar novo
- Token GitHub sem scope → Adicionar `repo` + `read:org`

**Como ver o erro:**
1. Clicar no workflow que falhou
2. Expandir o step que deu erro (tem um ❌ vermelho)
3. Ler a mensagem de erro
4. Me mandar print se não souber resolver

### Workflow completa mas dashboard não aparece

**Causa:** GitHub Pages não ativado ou branch errada

**Solução:**
1. Settings → Pages
2. Verificar se está em "gh-pages" / "/ (root)"
3. Aguardar 2-3 minutos
4. Hard refresh (Ctrl + Shift + R)

---

## 📞 Próximo Passo AGORA

**Configure os 3 secrets e rode o workflow!**

1. Secrets: https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/secrets/actions
2. Actions: https://github.com/ti-corp-picpay/germinares-health-dashboard/actions

**Quando o workflow completar, me chama que eu valido o resultado com você!** 🚀

---

**Criado em:** 25/03/2026 11:45 BRT  
**Próxima atualização automática:** Todo dia útil às 09:00 BRT
