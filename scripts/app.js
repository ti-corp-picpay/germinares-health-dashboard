// === APP.JS v3 - Full context, units, links, methodology ===

// Stats
const sau=G.filter(g=>g.hc==='saudavel').length;
const ate=G.filter(g=>g.hc==='atencao').length;
const ris=G.filter(g=>g.hc==='risco').length;
const avgHS=Math.round(G.reduce((s,g)=>s+g.hs,0)/G.length*10)/10;
const prodPct=Math.round((G.filter(g=>g.jd>0||g.gp>0).length)/G.length*100);
const riskPct=Math.round(ris/G.length*100);
const avgDone=Math.round(G.reduce((s,g)=>s+g.jd,0)/G.length*10)/10;
const ghMapped=G.filter(g=>g.gu).length;
const totalPRs=G.reduce((s,g)=>s+g.gp,0);
const totalMerged=G.reduce((s,g)=>s+g.gm,0);
const totalReviews=G.reduce((s,g)=>s+g.gr,0);

document.getElementById('kAvgHS').textContent=avgHS;
document.getElementById('kProd').textContent=prodPct+'%';
document.getElementById('kRisk').textContent=riskPct+'%';
document.getElementById('kAvgDone').textContent=avgDone;
document.getElementById('hSau').textContent=sau;
document.getElementById('hAte').textContent=ate;
document.getElementById('hRis').textContent=ris;

// Helper: Jira JQL link for a user
function jiraLink(email){return 'https://picpay.atlassian.net/issues/?jql=assignee%3D%22'+encodeURIComponent(email)+'%22%20AND%20updated%20%3E%3D%20-30d';}
function jiraProjectLink(proj){return 'https://picpay.atlassian.net/jira/software/projects/'+proj+'/board';}
function ghUserLink(user){return 'https://github.com/'+user;}
function ghPrsLink(user){return 'https://github.com/pulls?q=is%3Apr+author%3A'+user+'+org%3APicPay+is%3Aclosed';}
function ghReviewsLink(user){return 'https://github.com/pulls?q=is%3Apr+reviewed-by%3A'+user+'+org%3APicPay';}

// Alerts
const alertList=document.getElementById('alertList');
const inact=G.filter(g=>g.al.some(a=>a.includes('Inativo'))).length;
const agingCount=G.filter(g=>g.al.some(a=>a.includes('parada'))).length;
const wipHi=G.filter(g=>g.al.some(a=>a.includes('WIP alto'))).length;
const noAct=G.filter(g=>g.al.some(a=>a.includes('Sem atividade'))&&!g.al.some(a=>a.includes('Inativo'))).length;
const topCount=G.filter(g=>g.al.some(a=>a.includes('Top performer'))).length;

const alertsArr=[
{icon:'🔴',text:'<strong>'+inact+' germinares inativos</strong> — nenhuma issue movimentada no Jira e nenhum PR no GitHub nos ultimos 30 dias',count:inact,cls:'crit',action:'Verificar alocacao e acesso ao Jira'},
{icon:'🟠',text:'<strong>'+agingCount+' germinares com issues paradas</strong> — pelo menos 1 issue atribuida sem movimentacao ha mais de 21 dias corridos no Jira',count:agingCount,cls:'crit',action:'Issue cleanup com o time'},
{icon:'🟡',text:'<strong>'+noAct+' germinares sem atividade recente</strong> — tem issues atribuidas mas nenhuma movimentacao nos ultimos 7 dias',count:noAct,cls:'warn',action:'Check-in com mentor'},
{icon:'⚠️',text:'<strong>'+wipHi+' germinares com WIP alto</strong> — mais de 5 issues no status "In Progress" simultaneamente no Jira',count:wipHi,cls:'warn',action:'Limitar WIP a 3'},
{icon:'🟢',text:'<strong>'+topCount+' top performers</strong> — completion rate acima de 80% com mais de 10 issues concluidas no periodo',count:topCount,cls:'good',action:'Reconhecer e usar como mentores'}
];
alertsArr.filter(a=>a.count>0).forEach(a=>{
alertList.innerHTML+='<div class="al-item '+a.cls+'"><span class="al-icon">'+a.icon+'</span><span class="al-text">'+a.text+'<br><span style="color:var(--gr);font-weight:600;font-size:11px">Acao → '+a.action+'</span></span><span class="al-count">'+a.count+'</span></div>';
});

// Projects bars
const projBars=document.getElementById('projBars');
if(projBars && P && P.length){
const mx=Math.max(...P.map(p=>p.c));
const cl=['#21C25E','#3B82F6','#8B5CF6','#F5A623','#EF4444','#06B6D4','#EC4899','#F97316','#14B8A6','#6366F1','#84CC16','#F43F5E','#22D3EE','#A855F7','#EAB308'];
P.forEach((p,i)=>{const w=Math.round(p.c/mx*100);
projBars.innerHTML+='<div class="bar-row"><div class="bar-nm"><a href="'+jiraProjectLink(p.n)+'" target="_blank" style="color:var(--bl);text-decoration:none" title="Abrir board do projeto '+p.n+' no Jira">'+p.n+' ↗</a></div><div class="bar-tr"><div class="bar-fl" style="width:'+w+'%;background:'+cl[i%cl.length]+'">'+p.c+' issues</div></div></div>';
});}

// Table
let sC='r',sA=true,cF='all',sT='',cP=1;const PP=25;
function gF(){let d=[...G];
if(sT){const s=sT.toLowerCase();d=d.filter(r=>r.n.toLowerCase().includes(s)||r.e.toLowerCase().includes(s));}
if(cF==='inativo')d=d.filter(r=>r.al.some(a=>a.includes('Inativo')));
else if(cF==='gh')d=d.filter(r=>r.gp>0||r.gr>0);
else if(cF!=='all')d=d.filter(r=>r.hc===cF);
d.sort((a,b)=>{let x=a[sC],y=b[sC];if(typeof x==='string')return sA?x.localeCompare(y):y.localeCompare(x);return sA?(x||0)-(y||0):(y||0)-(x||0);});
return d;}

function hsColor(v){return v>=80?'#86efac':v>=60?'#fcd34d':'#fca5a5';}
function hsCls(hc){return{saudavel:'hs-sau',atencao:'hs-ate',risco:'hs-ris'}[hc]||'';}
function hsLabel(hc){return{saudavel:'Saudavel',atencao:'Atencao',risco:'Risco'}[hc]||'';}

function rT(){
const f=gF();const tp=Math.ceil(f.length/PP);if(cP>tp)cP=tp||1;
const s2=(cP-1)*PP;const pg=f.slice(s2,s2+PP);const tb=document.getElementById('tB');tb.innerHTML='';
pg.forEach(r=>{
const alTags=r.al.slice(0,2).map(a=>'<span class="at">'+a.substring(0,25)+'</span>').join('');
const dsaTxt=r.dsa<1?'hoje':r.dsa<2?'ontem':Math.round(r.dsa)+' dias';
const dsaCol=r.dsa<=3?'#86efac':r.dsa<=7?'#fcd34d':'#fca5a5';
const guTag=r.gu?' <a href="'+ghUserLink(r.gu)+'" target="_blank" style="color:#67e8f9;font-size:9px;text-decoration:none" onclick="event.stopPropagation()" title="Abrir perfil no GitHub">@'+r.gu+'</a>':'';
tb.innerHTML+='<tr onclick="showModal(\''+r.e+'\')" title="Clique para ver ficha completa">'
+'<td>'+r.r+'</td>'
+'<td style="font-weight:600"><a href="'+jiraLink(r.e)+'" target="_blank" style="color:var(--tx);text-decoration:none" title="Ver todas as issues deste germinar no Jira (ultimos 30 dias)" onclick="event.stopPropagation()">'+r.n+' ↗</a>'+guTag+'</td>'
+'<td><span class="hs-badge '+hsCls(r.hc)+'">'+r.hs+'</span></td>'
+'<td style="color:#86efac;font-weight:700">'+r.jd+'</td>'
+'<td style="color:'+(r.ji>5?'#fca5a5':r.ji>3?'#fcd34d':'#93c5fd')+'">'+r.ji+'</td>'
+'<td style="color:#fcd34d">'+r.jo+'</td>'
+'<td>'+(r.jcy>0?r.jcy+'d':'—')+'</td>'
+'<td style="border-left:2px solid rgba(6,182,212,0.15);color:#67e8f9;font-weight:'+(r.gp>0?'700':'400')+'">'+r.gp+'</td>'
+'<td style="color:#67e8f9">'+r.gm+'</td>'
+'<td style="color:#d8b4fe">'+r.gr+'</td>'
+'<td style="color:'+dsaCol+'">'+dsaTxt+'</td>'
+'<td>'+alTags+'</td></tr>';
});
const p2=document.getElementById('pg');
p2.innerHTML='<span style="color:var(--mu);font-size:10px;padding:4px">'+f.length+' germinares encontrados</span>';
for(let i=1;i<=tp;i++){p2.innerHTML+='<button class="pb'+(i===cP?' a':'')+'" onclick="cP='+i+';rT()">'+i+'</button>';}
}

document.querySelectorAll('th[data-o]').forEach(th=>{th.onclick=()=>{const c=th.dataset.o;if(sC===c)sA=!sA;else{sC=c;sA=c==='r';}cP=1;rT();};});
document.getElementById('sB').oninput=e=>{sT=e.target.value;cP=1;rT();};
document.querySelectorAll('.fb').forEach(b=>{b.onclick=()=>{document.querySelectorAll('.fb').forEach(x=>x.classList.remove('a'));b.classList.add('a');cF=b.dataset.f;cP=1;rT();};});
function filterBy(f){cF=f;document.querySelectorAll('.fb').forEach(x=>x.classList.toggle('a',x.dataset.f===f));cP=1;rT();document.getElementById('ranking').scrollIntoView({behavior:'smooth'});}
rT();

// MODAL - Ficha Individual
function showModal(email){
const g=G.find(x=>x.e===email);if(!g)return;
const m=document.getElementById('modalContent');
const jl=jiraLink(g.e);
const ghLink=g.gu?ghUserLink(g.gu):null;
const ghPr=g.gu?ghPrsLink(g.gu):null;
const ghRv=g.gu?ghReviewsLink(g.gu):null;

const dims=[
{name:'Entrega',emoji:'📦',val:g.d1,color:'var(--gr)',
 calc:'(issues done x 2) + (PRs merged x 3), max 100',
 detail:'<strong>'+g.jd+'</strong> issues done no Jira + <strong>'+g.gm+'</strong> PRs merged no GitHub',
 tip:'Mede volume de entregas concluidas. Issues done vem do status Done/Resolved/Closed no Jira. PRs merged vem do GitHub (state=closed com merged_at).'},
{name:'Eficiencia',emoji:'⚡',val:g.d2,color:'var(--bl)',
 calc:'Baseado no cycle time medio em dias. ≤3d=100, ≤7d=80, ≤14d=60, ≤21d=40, >21d=20',
 detail:'Cycle time medio: <strong>'+(g.jcy>0?g.jcy+' dias':'sem dados (nenhuma issue resolvida)')+'</strong>',
 tip:'Cycle time = dias entre a criacao da issue (campo Created) e a resolucao (campo Resolution Date) no Jira. Menor = mais eficiente.'},
{name:'Consistencia',emoji:'📅',val:g.d3,color:'var(--pu)',
 calc:'(semanas com atividade / 4 semanas) x 100',
 detail:'<strong>'+g.aw+' de 4 semanas</strong> tiveram pelo menos 1 issue movimentada',
 tip:'Divide os 30 dias em 4 semanas e conta em quantas houve pelo menos 1 issue com campo Updated alterado. 4/4 = 100, 3/4 = 75, etc.'},
{name:'Atividade',emoji:'🔥',val:g.d4,color:'var(--cy)',
 calc:'Baseado em dias desde ultima atividade. ≤1d=100, ≤3d=85, ≤7d=65, ≤14d=40, depois decresce',
 detail:'Ultima atividade: <strong>'+(g.dsa<1?'hoje':g.dsa<2?'ontem':'ha '+Math.round(g.dsa)+' dias')+'</strong>',
 tip:'Pega a data mais recente do campo Updated entre todas as issues atribuidas no Jira. Quanto mais recente, melhor.'},
{name:'Qualidade',emoji:'✅',val:g.d5,color:'var(--or)',
 calc:'(completion_rate x 0.6) + (aging_score x 0.4). Completion = done/total. Aging: ≤7d=100, ≤14d=75, ≤21d=50, >21d=25',
 detail:'Completion: <strong>'+g.jc+'%</strong> ('+g.jd+' done de '+g.jt+' total). Maior aging: <strong>'+(g.ja>0?Math.round(g.ja)+' dias':'nenhum')+'</strong>',
 tip:'Combina % de conclusao com penalidade por issues antigas abertas. Issue com aging = dias desde Created sem Resolution Date.'},
{name:'Carga (WIP)',emoji:'📊',val:g.d6,color:'var(--yl)',
 calc:'WIP 1-3=100, 4-5=70, >5 decresce 15 por item extra. Zero sem done=0',
 detail:'<strong>'+g.ji+' issues</strong> em status In Progress agora',
 tip:'Conta issues com status contendo "progress/review/test/dev/waiting/analysis" no Jira. Ideal = 2 a 3. Muito WIP = context switching = baixa entrega.'}
];

const maxWk=Math.max(...g.wk,1);
const semLabels=['Semana 1<br><small>(mais antiga)</small>','Semana 2','Semana 3','Semana 4<br><small>(atual)</small>'];
const wkBars=g.wk.map((w,i)=>'<div style="flex:1;text-align:center"><div style="height:60px;display:flex;align-items:flex-end;justify-content:center"><div style="width:75%;background:var(--gr);border-radius:4px 4px 0 0;height:'+Math.max(3,w/maxWk*55)+'px;opacity:'+(w>0?1:0.12)+'"></div></div><div style="font-size:9px;color:var(--mu);margin-top:4px">'+semLabels[i]+'</div><div style="font-size:12px;font-weight:700;color:'+(w>0?'var(--tx)':'var(--mu)')+'">'+w+' <small style="font-weight:400;color:var(--mu)">issues</small></div></div>').join('');

let h='<button class="modal-close" onclick="closeModal()">&times;</button>';
h+='<h2 style="font-size:24px">'+g.n+'</h2>';
h+='<div class="sub" style="line-height:1.8">';
h+='📧 <a href="mailto:'+g.e+'" style="color:var(--mu)">'+g.e+'</a><br>';
h+='🟢 Jira: <a href="'+jl+'" target="_blank" style="color:var(--gr)">Ver issues deste germinar ↗</a><br>';
if(g.gu){h+='🔵 GitHub: <a href="'+ghLink+'" target="_blank" style="color:#67e8f9">@'+g.gu+' ↗</a> · <a href="'+ghPr+'" target="_blank" style="color:#67e8f9">PRs ↗</a> · <a href="'+ghRv+'" target="_blank" style="color:#67e8f9">Reviews ↗</a><br>';}
else{h+='🔵 GitHub: <span style="color:var(--mu);font-style:italic">Username nao mapeado — dados GitHub indisponiveis</span><br>';}
h+='📁 Projetos: '+(g.jp.filter(x=>x).map(p=>'<a href="'+jiraProjectLink(p)+'" target="_blank" style="color:var(--gr);text-decoration:none">'+p+' ↗</a>').join(', ')||'<span style="color:var(--mu)">nenhum projeto encontrado</span>');
h+='</div>';

// Score
h+='<div class="score-big" style="color:'+hsColor(g.hs)+'">'+g.hs+'<span style="font-size:22px;color:var(--mu)">/100</span></div>';
h+='<div class="score-label"><span class="hs-badge '+hsCls(g.hc)+'">'+hsLabel(g.hc)+'</span></div>';

// Dimensions breakdown
h+='<h3 style="font-size:14px;font-weight:700;margin:20px 0 6px">📐 Breakdown do Health Score</h3>';
h+='<p style="font-size:10px;color:var(--mu);margin-bottom:12px">Cada dimensao vai de 0 a 100. O score final e a media ponderada (pesos indicados). Clique em "como calcula?" pra ver a formula.</p>';
h+='<div class="dim-grid">';
dims.forEach(d=>{
h+='<div class="dim-card">';
h+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">';
h+='<div class="dim-name">'+d.emoji+' '+d.name+'</div>';
h+='<div style="font-size:18px;font-weight:800;color:'+d.color+'">'+d.val+'<span style="font-size:10px;color:var(--mu)">/100</span></div>';
h+='</div>';
h+='<div class="dim-bar-track"><div class="dim-bar-fill" style="width:'+d.val+'%;background:'+d.color+'"></div></div>';
h+='<div style="font-size:11px;color:var(--tx);margin-top:6px">'+d.detail+'</div>';
h+='<details style="margin-top:4px"><summary style="font-size:9px;color:var(--bl);cursor:pointer">Como calcula?</summary><div style="font-size:9px;color:var(--mu);margin-top:4px;padding:6px;background:rgba(255,255,255,0.03);border-radius:4px"><strong>Formula:</strong> '+d.calc+'<br><strong>Fonte:</strong> '+d.tip+'</div></details>';
h+='</div>';});
h+='</div>';

// JIRA metrics
h+='<div style="margin-top:20px;padding:16px;background:rgba(33,194,94,0.05);border:1px solid rgba(33,194,94,0.15);border-radius:12px">';
h+='<h3 style="font-size:13px;font-weight:700;margin-bottom:4px">🟢 Metricas Jira</h3>';
h+='<p style="font-size:10px;color:var(--mu);margin-bottom:12px">Fonte: <a href="'+jl+'" target="_blank" style="color:var(--gr)">picpay.atlassian.net ↗</a> · JQL: assignee = "'+g.e+'" AND updated >= -30d</p>';
h+='<div class="metrics-grid">';
h+='<div class="metric"><div class="mv" style="color:#86efac">'+g.jd+'</div><div class="ml"><strong>Issues Done</strong><br>Issues com status Done, Resolved ou Closed no Jira nos ultimos 30 dias</div></div>';
h+='<div class="metric"><div class="mv" style="color:#93c5fd">'+g.ji+'</div><div class="ml"><strong>Issues em WIP</strong><br>Issues com status In Progress, In Review, In QA ou similar agora</div></div>';
h+='<div class="metric"><div class="mv" style="color:#fcd34d">'+g.jo+'</div><div class="ml"><strong>Issues Pendentes</strong><br>Issues com status To Do, Backlog, Open ou similar</div></div>';
h+='<div class="metric"><div class="mv">'+g.jt+'</div><div class="ml"><strong>Total Atribuidas</strong><br>Soma: done ('+g.jd+') + wip ('+g.ji+') + pendentes ('+g.jo+')</div></div>';
h+='<div class="metric"><div class="mv">'+(g.jcy>0?g.jcy+'<small style="color:var(--mu)"> dias</small>':'—')+'</div><div class="ml"><strong>Cycle Time</strong><br>'+(g.jcy>0?'Media em dias entre Created e Resolution Date das issues resolvidas':'Nenhuma issue resolvida no periodo — sem dados de cycle time')+'</div></div>';
h+='<div class="metric"><div class="mv">'+g.jc+'<small style="color:var(--mu)">%</small></div><div class="ml"><strong>Completion Rate</strong><br>'+g.jd+' done / '+g.jt+' total = '+g.jc+'% de conclusao</div></div>';
h+='</div></div>';

// GITHUB metrics
h+='<div style="margin-top:12px;padding:16px;background:rgba(6,182,212,0.05);border:1px solid rgba(6,182,212,0.15);border-radius:12px">';
h+='<h3 style="font-size:13px;font-weight:700;margin-bottom:4px">🔵 Metricas GitHub</h3>';
if(g.gu){
h+='<p style="font-size:10px;color:var(--mu);margin-bottom:12px">Fonte: <a href="'+ghPr+'" target="_blank" style="color:#67e8f9">github.com/PicPay ↗</a> · Busca: author:'+g.gu+' org:PicPay created:>30 dias</p>';
h+='<div class="metrics-grid">';
h+='<div class="metric"><div class="mv" style="color:#67e8f9">'+g.gp+'</div><div class="ml"><strong>PRs Abertos</strong><br>Pull Requests criados por @'+g.gu+' na org PicPay nos ultimos 30 dias</div></div>';
h+='<div class="metric"><div class="mv" style="color:#67e8f9">'+g.gm+'</div><div class="ml"><strong>PRs Merged</strong><br>PRs que foram aprovados em code review e integrados ao branch principal</div></div>';
h+='<div class="metric"><div class="mv" style="color:#d8b4fe">'+g.gr+'</div><div class="ml"><strong>Code Reviews</strong><br><a href="'+ghRv+'" target="_blank" style="color:#d8b4fe">Reviews feitos ↗</a> em PRs de outros desenvolvedores</div></div>';
h+='</div>';
}else{
h+='<div style="padding:16px;text-align:center;color:var(--mu);font-size:12px">⚠️ Username GitHub nao mapeado para este germinar.<br>O email <strong>'+g.e+'</strong> nao corresponde a nenhum username encontrado na org PicPay.<br>Dados de PRs, commits e reviews nao estao disponiveis.</div>';
}
h+='</div>';

// Weekly activity
h+='<h3 style="font-size:13px;font-weight:700;margin:20px 0 4px">📈 Atividade por Semana</h3>';
h+='<p style="font-size:10px;color:var(--mu);margin-bottom:10px">Quantidade de issues com campo Updated alterado em cada semana (Jira). Mostra se o germinar tem ritmo regular ou picos.</p>';
h+='<div style="display:flex;gap:8px;align-items:flex-end;margin-bottom:16px">'+wkBars+'</div>';

// Alerts
if(g.al.length>0){
h+='<h3 style="font-size:13px;font-weight:700;margin-bottom:8px">🚨 Alertas</h3>';
h+='<div class="modal-alerts">';
g.al.forEach(a=>{const cls=a.includes('Inativo')||a.includes('parada')?'crit':a.includes('WIP')||a.includes('Sem atividade')?'warn':a.includes('Top')||a.includes('Reviewer')?'good':'info';
h+='<div class="al-item '+cls+'"><span class="al-text">'+a+'</span></div>';});
h+='</div>';}

// Footer with data context
h+='<div style="margin-top:16px;padding:10px;background:var(--card);border-radius:8px;font-size:10px;color:var(--mu);line-height:1.6">';
h+='📅 Periodo: ultimos 30 dias · Extraido em: '+new Date().toLocaleDateString('pt-BR')+' · ';
h+='Ultima atividade Jira: <strong>'+(g.dsa<1?'hoje':'ha '+Math.round(g.dsa)+' dias')+'</strong> · ';
h+='Semanas ativas: <strong>'+g.aw+'/4</strong>';
h+='</div>';

m.innerHTML=h;
document.getElementById('modal').classList.add('show');
}
function closeModal(){document.getElementById('modal').classList.remove('show');}
document.getElementById('modal').onclick=e=>{if(e.target.id==='modal')closeModal();};
document.onkeydown=e=>{if(e.key==='Escape')closeModal();};

// Insights
const insList=document.getElementById('insightsList');
const topPerfs=G.filter(g=>g.hs>=80).sort((a,b)=>b.hs-a.hs);
const topNames=topPerfs.slice(0,3).map(g=>'<strong>'+g.n+'</strong> ('+g.hs+'/100)').join(', ');

const insArr=[
{cls:'cr',h:'🔴 '+inact+' germinares completamente inativos ('+Math.round(inact/216*100)+'%)',p:'Nenhuma issue movimentada no Jira e nenhum PR no GitHub em 30 dias.'},
{cls:'wr',h:'🟡 '+agingCount+' com issues paradas ha mais de 21 dias no Jira',p:'Pode ser bloqueio tecnico, falta de apoio ou issue abandonada.'},
{cls:'su',h:'🟢 Destaques: '+topNames,p:'Entregas consistentes, bom cycle time, atividade regular.'},
{cls:'in',h:'📊 GitHub: '+ghMapped+'/216 mapeados ('+Math.round(ghMapped/216*100)+'%)',p:'Para cobertura total, criar um GitHub Team na org PicPay ou obter lista de usernames.'},
{cls:'in',h:'📈 Proximos passos',p:'1. Mapear todos os GitHub usernames<br>2. Adicionar squad/BU/mentor por germinar<br>3. Automatizar extracao semanal<br>4. Cruzar com dados de mentores'}
];
insArr.forEach(i=>{insList.innerHTML+='<div class="ins '+i.cls+' fu"><h4>'+i.h+'</h4><p>'+i.p+'</p></div>';});

// Nav
const ss=['exec','health','alerts','jira','github','ranking','methodology','insights'];
const ds=document.querySelectorAll('.d');
ds.forEach(d=>d.onclick=()=>{const el=document.getElementById(d.dataset.s);if(el)el.scrollIntoView({behavior:'smooth'});});
const ob=new IntersectionObserver(e=>{e.forEach(x=>{
if(x.isIntersecting){ds.forEach(d=>d.classList.toggle('a',d.dataset.s===x.target.id));}
if(x.isIntersecting&&x.target.classList.contains('fu'))x.target.classList.add('v');
});},{threshold:0.15});
ss.forEach(s=>{const el=document.getElementById(s);if(el)ob.observe(el);});
document.querySelectorAll('.fu').forEach(el=>ob.observe(el));
