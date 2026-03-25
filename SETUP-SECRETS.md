# 🔐 Configuração de Secrets — GitHub Actions

Para o workflow funcionar, você precisa adicionar 3 secrets no repositório.

**URL:** https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/secrets/actions

---

## 📝 Secrets Necessários

### 1. **JIRA_EMAIL**
- **Valor:** Seu email Atlassian (ex: `natali.lee@picpay.com`)
- **Onde usar:** Autenticação na API do Jira

### 2. **JIRA_TOKEN**
- **Valor:** API Token do Jira
- **Como gerar:**
  1. Acesse: https://id.atlassian.com/manage-profile/security/api-tokens
  2. Clique em "Create API token"
  3. Dê um nome (ex: "Germinares Dashboard")
  4. Copie o token gerado
  5. Cole como secret no GitHub

### 3. **GH_PAT** (GitHub Personal Access Token)
- **Valor:** Token de acesso pessoal do GitHub
- **Como gerar:**
  1. Acesse: https://github.com/settings/tokens/new
  2. Nome: "Germinares Dashboard Workflow"
  3. Expiration: 90 days (ou No expiration)
  4. Selecione scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `read:org` (Read org and team membership)
  5. Clique em "Generate token"
  6. Copie o token (começa com `ghp_`)
  7. Cole como secret no GitHub

---

## ✅ Checklist de Configuração

Após adicionar os 3 secrets:

- [ ] JIRA_EMAIL adicionado
- [ ] JIRA_TOKEN adicionado
- [ ] GH_PAT adicionado
- [ ] Secrets salvos (botão verde "Add secret")
- [ ] GitHub Pages ativado (Settings → Pages → Branch: gh-pages / root)

---

## 🚀 Executar o Workflow

### **Execução Manual (primeira vez):**

1. Vá em: https://github.com/ti-corp-picpay/germinares-health-dashboard/actions
2. Clique em "Update Germinares Dashboard v2"
3. Clique em "Run workflow" → "Run workflow" (botão verde)
4. Aguarde ~30-40min (extração GitHub é lenta por causa do rate limiting)
5. Acesse: https://ti-corp-picpay.github.io/germinares-health-dashboard/

### **Execução Automática:**
- Roda todo dia útil às 09:00 BRT (12:00 UTC)
- Dashboard sempre atualizado com dados frescos

---

## 🐛 Troubleshooting

### Workflow falha com "ERROR: JIRA_EMAIL and JIRA_TOKEN required"
→ Secrets não configurados ou com nome errado. Verificar Settings → Secrets.

### Workflow falha com "401 Unauthorized" (Jira)
→ JIRA_TOKEN expirado ou inválido. Gerar novo token.

### Workflow falha com "403 Rate Limit" (GitHub)
→ GH_PAT sem scope `read:org` ou limite de requests excedido. Aguardar 1h ou usar token com limite maior.

### GitHub Pages retorna 404
→ Branch `gh-pages` não foi criado ainda. Aguardar primeiro workflow completar.

---

## 📞 Suporte

Qualquer problema, chamar o Wolf! 🐺

**Criado em:** 25/03/2026  
**Mantido por:** Natali Lee
