# Guia Executivo — Germinares Health Dashboard

**Documento de referência para apresentação executiva**  
*Última atualização: 25/03/2026*

---

## 📊 O que é o Health Dashboard?

Ferramenta de análise quantitativa que avalia a **atividade e engajamento** de cada um dos 216 Germinares (estagiários e trainees) do PicPay.

Cada Germinar recebe um **Health Score de 0 a 100 pontos**, calculado automaticamente a partir de dados reais do Jira e GitHub dos últimos 30 dias.

**Link:** https://ti-corp-picpay.github.io/germinares-health-dashboard/

---

## 🎯 Objetivo Principal

**Responder:** "Como cada Germinar está — e onde o programa precisa atuar?"

### O que o dashboard NÃO É:
- ❌ Ranking de competência técnica
- ❌ Ferramenta de cobrança individual
- ❌ Métrica de performance para avaliação formal

### O que o dashboard É:
- ✅ Termômetro de **engajamento e atividade**
- ✅ Detector de **gaps de alocação ou acesso**
- ✅ Sinalizador de **necessidade de apoio**
- ✅ Ferramenta de **acompanhamento longitudinal**

⚠️ **Princípio fundamental:** Score baixo ≠ problema. Pode significar onboarding recente, férias, realocação ou tarefas em outro sistema.

---

## 📐 Health Score — Como Funciona

### Fórmula

```
Health Score = (Entrega × 25%) + (Eficiência × 20%) + (Consistência × 15%) 
             + (Atividade × 15%) + (Qualidade × 15%) + (WIP × 10%)
```

Cada dimensão vale de 0 a 100. O score final é a **média ponderada**.

---

## 🔍 As 6 Dimensões — Explicadas

### 1. 📦 Entrega (25% do score)

**O que mede:** Volume de trabalho concluído  
**Unidade:** Quantidade (issues + PRs)  
**Fórmula:** `(issues done × 2) + (PRs merged × 3)`, limitado a 100  

**Fontes de dados:**
- **Jira:** Issues com status Done, Resolved ou Closed
  - JQL: `assignee = "email" AND status IN (Done, Resolved, Closed) AND updated >= -30d`
- **GitHub:** Pull Requests com `state=closed` e `merged_at` preenchido
  - Search: `type:pr author:{username} org:PicPay is:merged created:>30d`

**Interpretação executiva:**
- **80-100 pontos:** Alta produtividade — entregou 20+ issues ou 10+ PRs
- **40-79 pontos:** Produtividade moderada — entregou entre 5 e 20 issues
- **0-39 pontos:** Baixa entrega — pode ser início de programa, bloqueio ou falta de alocação

**Como falar na apresentação:**
> "A dimensão Entrega mede quantas issues o Germinar efetivamente concluiu no Jira e quantos PRs foram integrados ao código. É a métrica mais direta de output."

---

### 2. ⚡ Eficiência (20% do score)

**O que mede:** Velocidade de conclusão (cycle time)  
**Unidade:** Dias (média)  
**Fórmula:** Baseado no cycle time médio:
- ≤ 3 dias → 100 pontos
- ≤ 7 dias → 80 pontos
- ≤ 14 dias → 60 pontos
- ≤ 21 dias → 40 pontos
- \> 21 dias → 20 pontos

**Fonte de dados:**
- **Jira:** Diferença em dias entre `Created` e `Resolution Date`
  - Só considera issues que têm `Resolution Date` preenchido
  - Faz a média de todas as issues resolvidas no período

**Interpretação executiva:**
- **80-100 pontos:** Resolve issues em menos de 1 semana — rápido
- **40-79 pontos:** 1 a 3 semanas por issue — prazo normal
- **0-39 pontos:** Mais de 3 semanas — pode indicar complexidade alta ou bloqueios

**Como falar na apresentação:**
> "Eficiência responde: quanto tempo o Germinar leva pra concluir uma issue do início ao fim? Cycle time baixo indica agilidade — mas contexto importa. Issues complexas naturalmente levam mais tempo."

---

### 3. 📅 Consistência (15% do score)

**O que mede:** Regularidade de atividade ao longo do tempo  
**Unidade:** Semanas ativas (de 4)  
**Fórmula:** `(semanas com atividade / 4) × 100`  
- 4 semanas ativas → 100 pontos
- 3 semanas ativas → 75 pontos
- 2 semanas ativas → 50 pontos
- 1 semana ativa → 25 pontos

**Fonte de dados:**
- **Jira:** Campo `Updated` — divide os 30 dias em 4 semanas de 7 dias
  - Semana ativa = pelo menos 1 issue teve o campo `Updated` alterado naquela semana

**Interpretação executiva:**
- **75-100 pontos:** Trabalha toda semana — ritmo regular
- **50-74 pontos:** Algumas semanas sem atividade — pode ser picos de demanda
- **0-49 pontos:** Atividade concentrada em 1-2 semanas — risco de burnout ou inatividade

**Como falar na apresentação:**
> "Consistência mede se o Germinar tem ritmo de trabalho regular ou se faz tudo em picos. Quem trabalha toda semana tende a entregar mais e com menos stress do que quem concentra tudo no final."

---

### 4. 🔥 Atividade (15% do score)

**O que mede:** Recência — quantos dias desde a última movimentação  
**Unidade:** Dias atrás  
**Fórmula:** Dias desde a última atividade:
- ≤ 1 dia → 100 pontos
- ≤ 3 dias → 85 pontos
- ≤ 7 dias → 65 pontos
- ≤ 14 dias → 40 pontos
- \> 14 dias → decresce progressivamente

**Fonte de dados:**
- **Jira:** Campo `Updated` mais recente entre todas as issues atribuídas
  - "Hoje" = alguma issue foi mexida hoje
  - "5 dias" = há 5 dias desde a última alteração em qualquer issue

**Interpretação executiva:**
- **85-100 pontos:** Ativo nos últimos 3 dias — engajado
- **40-84 pontos:** Última atividade há 4-14 dias — pode estar em outra tarefa
- **0-39 pontos:** Mais de 14 dias sem movimentação — risco de desengajamento

**Como falar na apresentação:**
> "Atividade é o nosso early warning system. Se um Germinar está há mais de 7 dias sem mexer em nenhuma issue, algo pode estar errado — falta de alocação, bloqueio técnico ou desengajamento."

---

### 5. ✅ Qualidade (15% do score)

**O que mede:** Taxa de conclusão + controle de aging  
**Unidade:** Percentual + dias  
**Fórmula:** `(completion_rate × 60%) + (aging_score × 40%)`
- **Completion rate:** `done / (done + wip + todo) × 100`
- **Aging score:** Issue aberta mais antiga — ≤7d→100, ≤14d→75, ≤21d→50, >21d→25

**Fonte de dados:**
- **Jira:** 
  - Completion: `done / total de issues atribuídas`
  - Aging: issues sem `Resolution Date` — dias desde `Created`

**Interpretação executiva:**
- **80-100 pontos:** Conclui o que começa (>80% completion) + sem issues abandonadas
- **50-79 pontos:** Boa conclusão mas tem issues paradas, ou completa pouco do que pega
- **0-49 pontos:** Muita issue iniciada e não concluída — dispersão ou sobrecarga

**Como falar na apresentação:**
> "Qualidade responde: o Germinar termina o que começa? Ou acumula issues abertas? Completion rate alto + baixo aging = foco e disciplina de finalização."

---

### 6. 📊 Carga de Trabalho / WIP (10% do score)

**O que mede:** Quantidade de issues simultâneas em andamento  
**Unidade:** Quantidade (issues)  
**Fórmula:** 
- 1-3 issues simultâneas → 100 pontos (ideal)
- 4-5 issues → 70 pontos
- \> 5 issues → perde 15 pontos por item adicional
- 0 issues em WIP mas tem entregas → 80 pontos

**Fonte de dados:**
- **Jira:** Issues com status `In Progress`, `In Review`, `In QA`, `Waiting`, `In Development`, `In Analysis`, etc.

**Interpretação executiva:**
- **80-100 pontos:** Carga balanceada (2-3 coisas por vez) — foco
- **40-79 pontos:** 4-6 coisas simultâneas — aceitável mas não ideal
- **0-39 pontos:** Mais de 6 issues em paralelo — risco de context switching e baixa conclusão

**Como falar na apresentação:**
> "WIP (Work in Progress) mede quantas bolas o Germinar está malabarando ao mesmo tempo. Pesquisas mostram que mais de 3 tarefas simultâneas reduz drasticamente a produtividade. Ideal: fazer menos coisas, mas terminar."

---

## 📊 KPIs do Dashboard — Glossário

### Visão Geral (primeira tela)

| KPI | O que mostra | Como é calculado | Valor atual |
|-----|--------------|------------------|-------------|
| **Health Score Médio** | Score médio de todos os 216 Germinares | Soma de todos os scores ÷ 216 | ~40-50 (varia) |
| **Taxa de Produtivos** | % que teve pelo menos 1 entrega (issue done OU PR) | (Germinares com ≥1 entrega) / 216 × 100 | ~81% |
| **% Em Risco** | % com score abaixo de 60 | (Germinares com score <60) / 216 × 100 | ~73% |
| **Média de Entregas** | Média de issues done por Germinar | Total de issues done ÷ 216 | ~7 issues |

---

### Distribuição de Saúde (segunda tela)

| Classificação | Range de Score | O que significa | Quantidade atual |
|---------------|----------------|-----------------|------------------|
| 🟢 **Saudável** | 80-100 pontos | Entregando bem, ritmo consistente, sem alertas críticos | 11 Germinares |
| 🟡 **Atenção** | 60-79 pontos | Produtivo mas com irregularidades ou pontos de melhoria | 47 Germinares |
| 🔴 **Risco** | 0-59 pontos | Baixa atividade, inatividade ou possível sobrecarga. **Inclui os 41 inativos.** | 158 Germinares |

**Importante:** A maioria em "Risco" é puxada pelos 41 inativos (score ~8). Excluindo-os, a distribuição melhora significativamente.

---

### Alertas Automáticos (terceira tela)

| Alerta | Critério | O que significa | Ação recomendada |
|--------|----------|-----------------|------------------|
| 🔴 **Inativos** | 0 issues E 0 PRs em 30 dias | Nenhuma movimentação em Jira ou GitHub | Verificar se está alocado em squad, se tem acesso ao Jira, ou se as tarefas estão em outro sistema |
| 🟠 **Issues Paradas** | Aging > 21 dias em pelo menos 1 issue | Issue atribuída há mais de 3 semanas sem resolução | Issue cleanup com o time — fechar o que não é mais relevante ou re-priorizar |
| 🟡 **Sem Atividade Recente** | Última atividade > 7 dias (mas tem issues) | Mais de 1 semana sem mexer em nenhuma issue | Check-in com mentor/gestor pra entender se há bloqueio |
| ⚠️ **WIP Alto** | Mais de 5 issues em "In Progress" | Muitas coisas simultâneas — risco de context switching | Limitar WIP a 3, priorizar conclusão |
| 🟢 **Top Performer** | Completion > 80% E done > 10 | Entrega alta e consistente | Reconhecer publicamente e considerar como mentor para Germinares em risco |

---

## 📈 Métricas Jira — Explicadas

### Issues Done
**O que é:** Quantidade de issues que o Germinar levou até o fim (status final) nos últimos 30 dias.

**Critérios:**
- Status = `Done`, `Resolved`, `Closed`, `Finalizado`, `Concluído` (case-insensitive)
- Issue atribuída ao Germinar (`assignee = email`)
- Campo `Updated` nos últimos 30 dias

**Link de consulta:**  
`https://picpay.atlassian.net/issues/?jql=assignee="email" AND status IN (Done,Resolved,Closed) AND updated>=-30d`

**Como interpretar:**
- **20+ issues:** Alta produtividade — acima da média
- **10-19 issues:** Produtividade normal
- **5-9 issues:** Abaixo da média — pode ser complexidade alta ou alocação parcial
- **0-4 issues:** Muito baixo — investigar causa

---

### Issues em WIP (Work in Progress)
**O que é:** Quantas issues o Germinar está fazendo **agora** (simultaneamente).

**Critérios:**
- Status contém: `In Progress`, `In Review`, `In QA`, `In Development`, `Waiting`, `In Analysis`, `In Test`, `In Deploy`, etc.
- Issue atribuída ao Germinar

**Ideal:** 2 a 3 issues simultâneas

**Como interpretar:**
- **1-3 issues:** Carga balanceada ✅
- **4-5 issues:** Aceitável mas não ideal ⚠️
- **6+ issues:** Risco de context switching e baixa conclusão 🔴

**Por quê isso importa:**  
Pesquisas em produtividade mostram que fazer mais de 3 coisas ao mesmo tempo reduz a taxa de conclusão em até 40%. WIP alto é o principal preditor de baixa entrega.

---

### Issues Pendentes (Todo)
**O que é:** Issues atribuídas mas ainda não iniciadas (em backlog).

**Critérios:**
- Status = `To Do`, `Open`, `Backlog`, `New`, `Aberto`, etc.
- Issue atribuída ao Germinar

**Como interpretar:**
- **0-5 pendentes:** Backlog saudável
- **6-15 pendentes:** Backlog grande — priorização pode ajudar
- **16+ pendentes:** Possível sobrecarga ou alocação excessiva

---

### Cycle Time
**O que é:** Tempo médio (em dias) que o Germinar leva pra concluir uma issue, do início ao fim.

**Cálculo:**
```
Cycle Time = (Resolution Date - Created Date) em dias
Média de todas as issues resolvidas no período
```

**Fontes:**
- `Created`: data de criação da issue
- `Resolution Date`: data em que a issue foi marcada como Done/Resolved

**Como interpretar:**
- **≤ 5 dias:** Rápido — tasks pequenas ou alta agilidade ⚡
- **5-10 dias:** Normal — dentro do esperado para a maioria dos times ✅
- **10-20 dias:** Lento — pode ser complexidade ou falta de apoio ⚠️
- **> 20 dias:** Muito lento — investigar bloqueios ou escopo mal definido 🔴

**Importante:** Cycle time longo nem sempre é ruim. Depende do tipo de issue (bug vs feature), do projeto (refactoring vs manutenção) e do nível de senioridade.

---

### Completion Rate
**O que é:** Percentual de issues atribuídas que foram efetivamente concluídas.

**Fórmula:**
```
Completion Rate = (Done / Total Atribuídas) × 100
Total = Done + WIP + Pendentes
```

**Exemplo:**
- 15 done, 3 em WIP, 5 pendentes → Total = 23 → Completion = 15/23 = 65%

**Como interpretar:**
- **> 80%:** Alta taxa de conclusão — foca e termina o que começa ✅
- **60-79%:** Moderado — conclui a maioria mas tem backlog
- **< 60%:** Baixa conclusão — muita coisa iniciada, pouca finalizada 🔴

**Por quê isso importa:**  
Completion rate baixo indica dispersão ou sobrecarga. É comum ver Germinares com 30 issues atribuídas mas só 5 done — isso gera frustração e reduz a sensação de progresso.

---

### Aging (Máximo)
**O que é:** Quantos dias a issue **aberta mais antiga** do Germinar está parada.

**Cálculo:**
```
Aging = Hoje - Created (da issue sem Resolution Date mais antiga)
```

**Como interpretar:**
- **≤ 7 dias:** Sem issues antigas — tudo recente ✅
- **7-14 dias:** Aceitável — pode ser issue complexa em andamento
- **14-21 dias:** Atenção — issue pode estar travada ⚠️
- **> 21 dias:** Crítico — issue provavelmente abandonada ou esquecida 🔴

**Red flag:** Aging > 30 dias quase sempre indica issue que deveria ser fechada ou re-atribuída.

---

### Última Atividade
**O que é:** Quantos dias desde a última vez que **qualquer** issue atribuída ao Germinar foi mexida.

**Fonte:**
- Campo `Updated` mais recente entre todas as issues

**Como interpretar:**
- **Hoje/ontem:** Ativo agora ✅
- **2-7 dias:** Normal — pode estar focado em uma coisa só
- **8-14 dias:** Atenção — tempo longo sem movimentação ⚠️
- **> 14 dias:** Risco — pode estar desalocado ou bloqueado 🔴

---

## 🔵 Métricas GitHub — Explicadas

### PRs Abertos
**O que é:** Quantidade de Pull Requests criados pelo Germinar na org PicPay nos últimos 30 dias.

**Fonte:**
- GitHub Search API: `type:pr author:{username} org:PicPay created:>30d`

**Link de consulta:**  
`https://github.com/pulls?q=is:pr+author:{username}+org:PicPay`

**Como interpretar:**
- **10+ PRs:** Muito ativo no código
- **3-9 PRs:** Atividade moderada
- **1-2 PRs:** Baixa atividade
- **0 PRs:** Sem contribuição de código OU username não mapeado

---

### PRs Merged
**O que é:** PRs que foram aprovados em code review e integrados ao branch principal.

**Critério:**
- `state = closed` E `merged_at` preenchido

**Como interpretar:**
- **Merged / Abertos > 80%:** Alta taxa de aprovação — código de qualidade ✅
- **50-79%:** Normal — alguns PRs fechados sem merge (esperado)
- **< 50%:** Muitos PRs rejeitados ou fechados sem integrar — pode indicar qualidade ou alinhamento

---

### Code Reviews
**O que é:** Quantos PRs de **outros** desenvolvedores o Germinar revisou.

**Fonte:**
- GitHub Search: `type:pr reviewed-by:{username} org:PicPay`

**Link de consulta:**  
`https://github.com/pulls?q=is:pr+reviewed-by:{username}+org:PicPay`

**Como interpretar:**
- **10+ reviews:** Revisor ativo — cultura de colaboração 🌟
- **3-9 reviews:** Participa de code review moderadamente
- **1-2 reviews:** Baixa participação em revisões
- **0 reviews:** Não faz code review OU não mapeado

**Por quê isso importa:**  
Code review é uma das práticas mais eficazes de aprendizado. Germinares que revisam código aprendem mais rápido.

---

## ⚠️ Limitações Conhecidas

### 1. GitHub: Cobertura Parcial (39/216)
**Problema:** Apenas 18% dos Germinares foram mapeados no GitHub.

**Causa:** Usernames no GitHub não seguem padrão previsível do email corporativo.
- Tentamos: `nome-sobrenome`, `nomesobrenome`, `nome.sobrenome`
- Resultado: só 39 matches

**Impacto:** Métricas de PRs, merged e reviews são **parciais**.

**Solução:**
1. Criar um **GitHub Team** na org PicPay com todos os Germinares
2. Obter lista de usernames junto ao RH ou coordenação do programa
3. Rodar extração novamente com mapeamento completo

---

### 2. Score Reflete Atividade, Não Competência
**Problema:** Um score baixo pode ter múltiplas causas não relacionadas a performance.

**Causas de score baixo que NÃO são problema:**
- Germinar recém-chegado (onboarding)
- Férias ou afastamento no período
- Realocação de área (trocou de squad/projeto)
- Tarefas em outro sistema (planilha, Trello, etc.)
- Issues grandes que levam > 30 dias (ex: refactoring)

**Como mitigar:**  
Sempre **investigar contexto** antes de agir. Score é ponto de partida, não conclusão.

---

### 3. Dados do Jira Podem Estar Incompletos
**Problema:** Se o Germinar não atualiza o board do Jira, a atividade real dele fica invisível.

**Exemplo:** Germinar trabalha todo dia no código (commits diários) mas não move as issues no Jira → aparece como "inativo".

**Como mitigar:**  
Cruzar dados Jira + GitHub. Se tem PRs mas zero issues → desalinhamento entre código e board.

---

## 🎤 Roteiro de Apresentação Executiva

### Slide 1: Contexto
> "Temos 216 Germinares atuando em 124 projetos Jira. Até agora, a visibilidade sobre como cada um está era qualitativa — percepção de mentores. Este dashboard é a primeira análise **quantitativa** do programa."

### Slide 2: Health Score
> "Cada Germinar recebe um score de 0 a 100, calculado automaticamente a partir de 6 dimensões objetivas: volume de entregas, velocidade, consistência, recência de atividade, taxa de conclusão e carga de trabalho."

**Mostrar:** Explicação das 6 dimensões (usar o gráfico de pizza com pesos)

### Slide 3: Distribuição
> "Dos 216 Germinares: 11 estão saudáveis (80+), 47 em atenção (60-79) e 158 em risco (<60). Mas **atenção:** risco não significa problema. Score baixo pode ser onboarding, férias ou realocação."

**Mostrar:** Cards 🟢🟡🔴 com as quantidades

### Slide 4: Achados Críticos
> "**41 Germinares (19%)** não tiveram **nenhuma** movimentação em Jira ou GitHub nos últimos 30 dias. Isso é um gap de visibilidade — precisamos entender se é falta de alocação, acesso, ou se as tarefas estão em outro lugar."

**Mostrar:** Card de alerta vermelho dos inativos

### Slide 5: Outros Alertas
> "Além dos inativos, temos:
> - 124 Germinares com issues paradas há mais de 14 dias
> - 18 com WIP alto (sobrecarga potencial)
> - Apenas 39 mapeados no GitHub (dados de código são parciais)"

**Mostrar:** Grid de alertas

### Slide 6: Destaques Positivos
> "Nem tudo é problema. Temos **11 top performers** com score 80+ e entregas consistentes. Destaques:
> - **davi.santos**: score 93, ativo nas 4 semanas, 23 issues done
> - **geovanna.diniz**: 99 issues done, 95% completion rate
> - **gabriel.loureiro**: 100 PRs merged no GitHub em 30 dias"

**Mostrar:** Top 3 do ranking

### Slide 7: Ações Imediatas
> "O que fazer com esses dados:
> 1. **Investigar os 41 inativos** — é gap de alocação ou de visibilidade?
> 2. **Issue cleanup** com os times — 341 issues abertas há mais de 21 dias
> 3. **Mapear todos no GitHub** — criar um Team na org PicPay
> 4. **Rodar semanalmente** — acompanhar evolução ao longo do tempo"

### Slide 8: Disclaimer
> "⚠️ **Importante:** Este dashboard mede **atividade no sistema**, não competência técnica. Usá-lo como ferramenta de cobrança individual pode distorcer comportamentos — Germinares podem começar a inflar números em vez de focar em aprendizado.
>
> **Use como ferramenta de apoio,** não de pressão."

---

## 📋 Perguntas Frequentes (para a reunião)

### "Por que a maioria está em risco?"
**R:** Dos 158 em risco, 41 são inativos (score ~8). Isso puxa a média pra baixo. Se excluirmos os inativos, a distribuição fica mais equilibrada. Além disso, muitos Germinares têm score 50-59 (perto da linha de corte) — não são casos graves.

---

### "Score 40 é baixo ou normal?"
**R:** Depende. Score 40 significa que o Germinar teve **alguma atividade** mas com irregularidades — pode ser:
- Entregou poucas issues (5-8)
- Cycle time alto (>14 dias)
- Atividade concentrada em 1-2 semanas (não foi consistente)
- WIP alto ou baixa conclusão

**Contexto importa.** Se for um Germinar novo (1º mês), score 40 pode ser esperado.

---

### "O que fazer com quem tem score baixo?"
**R:** **Não cobrar — investigar.**

Roteiro:
1. Olhar os **alertas** específicos daquele Germinar (clicando na linha)
2. **Perguntar ao mentor:** "Você sabe o que esse Germinar está fazendo?"
3. **Checar alocação:** Ele está em algum squad? Tem tasks atribuídas?
4. **Verificar acesso:** Ele consegue abrir o Jira do projeto? Tem permissão no repo GitHub?

Só depois de entender o contexto, decidir se precisa de apoio técnico, realocação ou se está tudo bem (ex: férias).

---

### "Como usar isso no dia a dia?"
**R:** 3 usos principais:

1. **Weekly check-in com coordenação:** Olhar os alertas novos da semana
2. **1-on-1 mentor-Germinar:** Mostrar o score + breakdown das 6 dimensões pra discutir pontos de melhoria
3. **Acompanhamento longitudinal:** Rodar toda semana e ver quem melhorou, quem piorou, identificar tendências

---

### "Podemos usar isso pra avaliação formal?"
**R:** **Não recomendado** como métrica única.

Health Score pode **complementar** avaliação qualitativa (percepção do mentor, entregas de projeto, soft skills) mas **não deve ser o único critério**.

**Risco:** Se os Germinares souberem que o score impacta avaliação, eles podem:
- Pegar issues fáceis pra inflar o "done"
- Evitar issues complexas que aumentam o cycle time
- Atualizar issues sem razão só pra zerar o "sem atividade"

Isso **mata o propósito** do dashboard.

---

## 📝 Material de Apoio

### Para incluir na apresentação (slides sugeridos):

**Slide: "O que é o Health Score?"**
- Diagrama de pizza com os 6 pedaços (25%, 20%, 15%, 15%, 15%, 10%)
- Legenda: Entrega, Eficiência, Consistência, Atividade, Qualidade, WIP

**Slide: "Distribuição Atual"**
- 3 cards coloridos: 🟢 11 Saudáveis, 🟡 47 Atenção, 🔴 158 Risco
- Gráfico de barras com a distribuição

**Slide: "Alertas Críticos"**
- Lista com bullets:
  - 🔴 41 inativos (19%)
  - 🟠 124 com issues paradas >14 dias
  - 🟡 18 com WIP alto

**Slide: "Destaques"**
- Fotos/nomes dos top 3 performers
- Números: "99 issues done", "100 PRs merged", "score 93/100"

**Slide: "Próximos Passos"**
- Checklist com ações imediatas

---

## 🔗 Links de Referência

| Item | Link |
|------|------|
| **Dashboard** | https://ti-corp-picpay.github.io/germinares-health-dashboard/ |
| **Repositório** | https://github.com/ti-corp-picpay/germinares-health-dashboard |
| **Jira PicPay** | https://picpay.atlassian.net |
| **GitHub PicPay** | https://github.com/PicPay |
| **Adicionar Secrets** | https://github.com/ti-corp-picpay/germinares-health-dashboard/settings/secrets/actions |
| **GitHub Actions** | https://github.com/ti-corp-picpay/germinares-health-dashboard/actions |

---

*Documento gerado por Wolf 🐺 para Natali Lee · 25/03/2026*
